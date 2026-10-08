import { styleText } from "node:util";

type Level = "info" | "success" | "warn" | "error";

const LABELS: Readonly<Record<Level, string>> = {
  info: "INFO",
  success: "SUCCESS",
  warn: "WARN",
  error: "ERROR",
};

const COLORS: Readonly<Record<Level, Parameters<typeof styleText>[0]>> = {
  info: "gray",
  success: "green",
  warn: "yellow",
  error: "red",
};

export interface Logger {
  info(message: string): void;
  success(message: string): void;
  warn(message: string): void;
  error(message: string): void;
}

export function createLogger(scope: string): Logger {
  function write(level: Level, message: string): void {
    const time = new Date().toISOString().slice(11, 19);
    const label = styleText(COLORS[level], LABELS[level], { stream: process.stdout });
    process.stdout.write(`${time} [${scope}] ${label} ${message}\n`);
  }

  return {
    info(message) {
      write("info", message);
    },
    success(message) {
      write("success", message);
    },
    warn(message) {
      write("warn", message);
    },
    error(message) {
      write("error", message);
    },
  };
}
