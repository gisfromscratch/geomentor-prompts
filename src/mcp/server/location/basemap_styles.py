from enum import Enum
from typing import List, Dict

class BasemapCategory(Enum):
    """
    An enumeration representing different categories of basemaps.

    Attributes:
        STREETS: Basemaps that emphasize street and road networks.
        TOPOGRAPHY: Basemaps that highlight terrain and elevation features.
        SATELLITE: Basemaps that display satellite imagery.
        REFERENCE: Basemaps designed for reference and context, often minimalistic.
        CREATIVE: Basemaps with creative or artistic styles.
    """
    STREETS = "Streets"
    TOPOGRAPHY = "Topography"
    SATELLITE = "Satellite"
    REFERENCE = "Reference"
    CREATIVE = "Creative"

class BasemapSubStyle(Enum):
    """
    Enumeration of available basemap sub-styles for map rendering.

    Each member represents a specific visual style or theme for displaying map data.
    The sub-styles are grouped into categories such as:

    - Streets: Navigation, Navigation Night, Streets, Streets Night, Community
    - Topography: Outdoor, Oceans
    - Satellite: Imagery, Imagery Labels
    - Reference: Light Gray, Dark Gray, Human Geography, Human Geography Dark
    - Creative: Nova, Midcentury, Newspaper

    These styles can be used to customize the appearance of basemaps in mapping applications.
    """
    # Streets
    NAVIGATION = "navigation"
    NAVIGATION_NIGHT = "navigation-night"
    STREETS = "streets"
    STREETS_NIGHT = "streets-night"
    COMMUNITY = "community"
    # Topography
    OUTDOOR = "outdoor"
    OCEANS = "oceans"
    # Satellite
    IMAGERY = "imagery"
    IMAGERY_LABELS = "imagery-labels"
    # Reference
    LIGHT_GRAY = "light-gray"
    DARK_GRAY = "dark-gray"
    HUMAN_GEOGRAPHY = "human-geography"
    HUMAN_GEOGRAPHY_DARK = "human-geography-dark"
    # Creative
    NOVA = "nova"
    MIDCENTURY = "midcentury"
    NEWSPAPER = "newspaper"

    @staticmethod
    def from_string(style: str) -> 'BasemapSubStyle':
        """
        Convert a string to a BasemapSubStyle enum member.

        The input string must match the enum value (case-insensitive, hyphens allowed).

        Args:
            style: The string representation of the sub-style.

        Returns:
            The corresponding BasemapSubStyle enum member or the default sub-style.
        """
        try:
            # Try to match by value first (case-insensitive)
            for member in BasemapSubStyle:
                if member.value.lower() == style.lower():
                    return member
        except KeyError:
            return BasemapSubStyle.NAVIGATION

# Mapping of basemap categories to their supported sub-styles
SUPPORTED_BASEMAP_STYLES: Dict[BasemapCategory, List[BasemapSubStyle]] = {
    BasemapCategory.STREETS: [
        BasemapSubStyle.NAVIGATION,
        BasemapSubStyle.NAVIGATION_NIGHT,
        BasemapSubStyle.STREETS,
        BasemapSubStyle.STREETS_NIGHT,
        BasemapSubStyle.COMMUNITY,
    ],
    BasemapCategory.TOPOGRAPHY: [
        BasemapSubStyle.OUTDOOR,
        BasemapSubStyle.OCEANS,
    ],
    BasemapCategory.SATELLITE: [
        BasemapSubStyle.IMAGERY,
        BasemapSubStyle.IMAGERY_LABELS,
    ],
    BasemapCategory.REFERENCE: [
        BasemapSubStyle.LIGHT_GRAY,
        BasemapSubStyle.DARK_GRAY,
        BasemapSubStyle.HUMAN_GEOGRAPHY,
        BasemapSubStyle.HUMAN_GEOGRAPHY_DARK,
    ],
    BasemapCategory.CREATIVE: [
        BasemapSubStyle.NOVA,
        BasemapSubStyle.MIDCENTURY,
        BasemapSubStyle.NEWSPAPER,
    ],
}