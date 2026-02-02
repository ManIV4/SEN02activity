# UI/UX Design Documentation - Person 4

## Design Philosophy
* **Theme**: Steam-Inspired Dark UI to match the platform's aesthetic.
* **Visual Goal**: Reduce eye strain while providing a professional gaming look.

## Color Palette
| Element | Hex Code | Purpose |
| :--- | :--- | :--- |
| **Steam Blue** | `#66c0f4` | Headers, highlights, and links. |
| **Dark Navy** | `#1b2838` | Main background color. |
| **Positive** | `#5cb85c` | Sentiment scores 60% and above. |
| **Mixed** | `#f0ad4e` | Sentiment scores between 40-60%. |
| **Negative** | `#d9534f` | Sentiment scores below 40%. |

## Layout Structure
* **Header**: Contains the dashboard title and the 60s auto-refresh countdown.
* **Stat Cards**: A 3-column grid for Total Players, Games Tracked, and Avg Sentiment.
* **Game Cards**: Individual blocks for each game featuring rank badges and progress bars.
* **Trend Sections**: Bottom area displaying top Genres and Categories.

## Key Features
* **Responsive Design**: Adjusts from a 3-column grid on desktop to a single column on mobile.
* **Animations**: Stat cards feature a lift effect (`-5px`) on hover for interactivity.
* **Live Updates**: JavaScript fetches data every 60 seconds without a page reload.

---
**Designed by**: [Your Name]
**Date**: February 2026
