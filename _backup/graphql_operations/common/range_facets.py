RANGE_FACETS_FRAGMENT = """
   {
            name
            label
            order
            facetType
            ranges {
                count
                from
                includeFrom
                fromStr
                max
                min
                to
                includeTo
                toStr
                total
                label
                isSelected
            }
            statistics {
                max
                min
            }
        }
"""
