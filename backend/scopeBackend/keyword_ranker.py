# This file contains code to reorder the sources related to a query
# so that sources with higher primary & secondary keyword count
# and matches are prioritized

#takes in a primary keyword, array of secondary keywords, and the unranked queryset
def rank(primary_kw, secondary_kws, queryset):
    # 1. Reorder sources based on how many keywords were matched
    #   - the primary keyword match is most important so reorder on that basis first
    #   - then for every source, reorder based on how many secondary keywords were matched
    #   - return the final reordered set
    # 2. Reorder sources based on the highest count for every keyword
    #   - again priority is given to primary keyword so reorder first based on the amount
    #       of times the primary keyword appears in a given source
    #   - then for every source, store the counts for each secondary kw in a dictionary
    #       and reorder based on the cumulative counts
    #   - return the final reordered set 
    pass