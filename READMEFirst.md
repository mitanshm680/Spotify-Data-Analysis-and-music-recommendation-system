# Spotify Data Analysis and Music Recommendation System

## Project Overview
This project aims to analyze Spotify listening data and develop a personalized music recommendation system. The analysis focuses on understanding user listening behavior, correlating audio features with moods, and building a recommendation model based on user preferences.

## Libraries Used
- dplyr
- jsonlite
- readr
- stringr
- lubridate
- zoo
- stats
- ggplot2
- plotly
- reshape2
- kableExtra
- knitr
- rmarkdown
[NOTE - These libraries are required and need to be installed before running the Rmd files]

## Files Included
- **Data Files**:
  - `StreamingHistory_music_0.json`
  - `StreamingHistory_music_1.json`

- **R Markdown Files**:
  - `SpotifyProjectHTML.Rmd`
  - `SpotifyProjectPDF.Rmd`

    - *Purpose*: Both files contain the code and analysis for the project, but each is set up to generate different types of outputs.
    - *Differences*: 
        - **HTML**: Uses `plotly` for interactive visualizations since HTML allows for interactivity.
        - **PDF**: Uses `ggplot2` exclusively for static visualizations suitable for a PDF format, with the output in landscape orientation.

- **Generated Output Files**:
  - `SpotifyProjectHTML.html`: Interactive HTML document generated from `SpotifyProjectHTML.Rmd`.
  - `SpotifyProjectPDF.pdf`: Static PDF document generated from `SpotifyProjectPDF.Rmd`.

## Additional Notes
- The HTML output allows interactive exploration of data visualizations, leveraging `plotly`.
- The PDF output is formatted in landscape orientation for readability, with static plots via `ggplot2`.

Please refer to the HTML or PDF files for a complete overview of the analysis and findings.
