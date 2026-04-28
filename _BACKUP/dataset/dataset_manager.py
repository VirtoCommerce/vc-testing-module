import argparse
import json
import re
from enum import Enum
from json import JSONDecodeError
from pathlib import Path
from typing import Any, Callable, Literal

from inflection import camelize
from pydantic import BaseModel, ValidationError
from rich.console import Console
from rich.progress import Progress

from fixtures.auth import Auth
from fixtures.config import Config
from fixtures.webapi_client import WebAPISession
from logger.file_logger import FileLogger
from utils.run_progress import run_progress


class VariableType(Enum):
    ENV = "ENV"
    PAYLOAD_ITEM = "PAYLOAD_ITEM"


VAR_TYPES = "|".join(v.value for v in VariableType)
INTERPOLATION_PATTERN = re.compile(rf"\{{({VAR_TYPES}):([a-zA-Z0-9_]+)\}}")


class SeedRequest(BaseModel):
    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
    endpoint: str
    payload_type: Literal["array", "single"]
    data: list[dict[str, Any]]
    priority: int = 99999


class DatasetManager:
    base_dir: Path = Path(__file__).parent
    data_dir: Path = base_dir / "data"
    seed_requests: dict[str, SeedRequest] | None = None
    dataset: dict[str, dict[str, Any]] | None = None
    _console: Console = Console()
    _logger: FileLogger = FileLogger(
        "dataset_manager", base_dir / "dataset_manager.log"
    )
    _config: Config = Config()
    _auth: Auth = Auth(_config)
    _webapi_client: WebAPISession = WebAPISession(_config, _auth)

    def __init__(self) -> None:
        self.dataset: dict[str, list[dict[str, Any]]] = {}
        self._variable_resolvers: dict[
            VariableType, Callable[[str, dict[str, Any]], Any]
        ] = {
            VariableType.ENV: self._resolve_env,
            VariableType.PAYLOAD_ITEM: self._resolve_payload_item,
        }

    def _get_request_files_paths(self) -> list[Path]:
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Directory '{self.data_dir}' does not exist")

        files: list[Path] = list[Path](self.data_dir.glob("*.json"))

        if not files:
            raise FileNotFoundError(f"No JSON files found in '{self.data_dir}'")

        return files

    def _filter_requests(
        self, entities: list[str]
    ) -> tuple[dict[str, SeedRequest], list[str]]:
        if not entities:
            return self.seed_requests, []

        entity_set = set(entities)
        available = self.seed_requests.keys()

        found = {
            name: self.seed_requests[name] for name in entity_set if name in available
        }

        missing = list(entity_set - available)

        return found, missing

    def _resolve_env(self, variable_name: str, _: dict[str, Any]) -> Any:
        try:
            return self._config[variable_name]
        except KeyError as error:
            raise KeyError(f"ENV variable not found: {variable_name}") from error

    def _resolve_payload_item(self, variable_name: str, item: dict[str, Any]) -> Any:
        if not isinstance(item, dict):
            raise KeyError(
                f"PAYLOAD_ITEM requires dict payloads; got {type(item).__name__}"
            )
        try:
            return item[variable_name]
        except KeyError as error:
            raise KeyError(
                f"PAYLOAD_ITEM property not found in payload item: {variable_name}"
            ) from error

    def _resolve_variable(
        self, variable_type: str, variable_name: str, item: dict[str, Any]
    ) -> Any:
        try:
            variable_enum = VariableType(variable_type)
        except ValueError as error:
            raise KeyError(f"Unsupported variable type: {variable_type}") from error

        resolver = self._variable_resolvers.get(variable_enum)
        if resolver is None:
            raise KeyError(f"No resolver registered for variable type: {variable_type}")
        return resolver(variable_name, item)

    def _interpolate_string(self, value: str, item: dict[str, Any]) -> str:
        def replace(match: re.Match[str]) -> str:
            variable_type, variable_name = match.group(1), match.group(2)
            resolved_value = self._resolve_variable(variable_type, variable_name, item)
            return str(resolved_value)

        return INTERPOLATION_PATTERN.sub(replace, value)

    def _interpolate_env_string(self, value: str) -> str:
        def replace(match: re.Match[str]) -> str:
            variable_type, variable_name = match.group(1), match.group(2)
            if variable_type != VariableType.ENV.value:
                return match.group(0)
            resolved_value = self._resolve_env(variable_name, {})
            return str(resolved_value)

        return INTERPOLATION_PATTERN.sub(replace, value)

    def _interpolate_payload(self, value: Any, item: dict[str, Any]) -> Any:
        if isinstance(value, dict):
            return {
                key: self._interpolate_payload(nested, item)
                for key, nested in value.items()
            }
        if isinstance(value, list):
            return [self._interpolate_payload(nested, item) for nested in value]
        if isinstance(value, str):
            return self._interpolate_string(value, item)
        return value

    def _interpolate_env_payload(self, value: Any) -> Any:
        if isinstance(value, dict):
            return {
                key: self._interpolate_env_payload(nested)
                for key, nested in value.items()
            }
        if isinstance(value, list):
            return [self._interpolate_env_payload(nested) for nested in value]
        if isinstance(value, str):
            return self._interpolate_env_string(value)
        return value

    def load_requests(self) -> None:
        file_paths = self._get_request_files_paths()
        seed_requests: dict[str, SeedRequest] = {}

        def process(progress: Progress, task_id: int) -> None:
            for file_path in file_paths:
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        request = json.load(file)
                        seed_request = SeedRequest(**request)
                        seed_request.endpoint = self._interpolate_env_string(
                            seed_request.endpoint
                        )
                        seed_request.data = [
                            self._interpolate_env_payload(item)
                            for item in seed_request.data
                        ]
                        dataset_name = camelize(
                            file_path.stem, uppercase_first_letter=False
                        )
                        self.dataset[dataset_name] = seed_request.data
                except JSONDecodeError as error:
                    self._console.print(f"[red]{file_path.name}: invalid JSON[/red]")
                    self._logger.error(f"{file_path}: {error}")
                except ValidationError as error:
                    self._console.print(f"[red]{file_path.name}: invalid schema[/red]")
                    self._logger.error(f"{file_path}: {error}")
                except Exception as error:
                    self._console.print(f"[red]{file_path.name}: failed to load[/red]")
                    self._logger.error(f"{file_path}: {error}")
                else:
                    seed_requests[file_path.stem] = seed_request
                    self._logger.info(f"{file_path.name}: loaded successfully")
                finally:
                    progress.update(task_id, advance=1)

        run_progress("Loading dataset", len(file_paths), self._console, process)
        self.seed_requests = dict[str, SeedRequest](
            sorted(seed_requests.items(), key=lambda item: item[1].priority)
        )

    def seed(self, entities: list[str]) -> None:
        if self.seed_requests is None:
            self._console.print("[yellow]WARNING:No requests to seed[/yellow]")
            return

        requests, absent_entities = self._filter_requests(entities)

        if absent_entities:
            self._console.print(
                f"[yellow]WARNING: Entities not found: {', '.join(absent_entities)}[/yellow]"
            )
            if len(absent_entities) == len(requests.keys()):
                return

        self._console.print(f"Seeding datasets: {', '.join(requests.keys())}")

        total_operations: int = 0
        for request in requests.values():
            if request.payload_type == "array":
                total_operations += 1
            else:
                total_operations += len(request.data)

        if total_operations == 0:
            self._console.print(f"[yellow]WARNING: No payloads to seed[/yellow]")
            return

        def process(progress: Progress, task_id: int) -> None:
            self._auth.authenticate(
                username=self._config["ADMIN_USERNAME"],
                password=self._config["ADMIN_PASSWORD"],
            )

            def send_request(name: str, method: str, endpoint: str, body: Any) -> None:
                url = f"{method}: {self._config['BACKEND_BASE_URL']}{endpoint}"
                try:
                    self._webapi_client.request(method, endpoint, body)
                except Exception as error:
                    message = getattr(error, "message", repr(error))
                    self._console.print(
                        f"[red]ERROR: Failed to seed {name}: {url}[/red]"
                    )
                    self._logger.error(f"{name}: {url}\n{message}")
                else:
                    self._logger.info(f"{name}: {url}: seeded successfully")
                    self._logger.info(f"Payload: {body}")
                finally:
                    progress.update(task_id, advance=1)

            for name, request in requests.items():
                if request.payload_type == "array":
                    item_context = request.data[0] if request.data else {}
                    endpoint = self._interpolate_string(request.endpoint, item_context)
                    body = self._interpolate_payload(request.data, item_context)
                    send_request(name, request.method, endpoint, body)
                elif request.payload_type == "single":
                    for payload in request.data:
                        endpoint = self._interpolate_string(request.endpoint, payload)
                        body = self._interpolate_payload(payload, payload)
                        send_request(name, request.method, endpoint, body)

            self._auth.clear_token()

        run_progress("Seeding datasets", total_operations, self._console, process)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--seed",
        nargs="*",
        default=None,
        help="Optional list of dataset names to seed",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    dataset_manager = DatasetManager()
    dataset_manager.load_requests()

    if args.seed is not None:
        targets = None if not args.seed else args.seed
        dataset_manager.seed(targets)


if __name__ == "__main__":
    main()
