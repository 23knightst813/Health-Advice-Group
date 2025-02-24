> ***Git Log***
> - **09e7af2** 2025-02-25 10:51:40 - Add localization support for weather tips and implement location testing in JavaScript
> - **444b718** 2025-02-17 15:18:38 - Merge pull request #13 from 23knightst813/fix-flash-error
> - **60762e5** 2025-02-17 15:18:29 - Fix flash error by using logging
> - **d4a95fe** 2025-02-14 11:45:05 - Refactor rate limiting responses in RateLimit.py to use JSON instead of flash messages and redirects for improved API compatibility
> - **d970188** 2025-02-14 11:40:58 - Add flash and redirect imports to RateLimit.py for enhanced user feedback
> - **abc5af3** 2025-02-14 11:40:08 - Implement rate limiting for user registration, login, and various routes; add Flask-Limiter and Redis to requirements
> - **5346e14** 2025-02-14 11:14:46 - Add user IP logging and remove logging for 404 errors
> - **855fd24** 2025-02-14 11:07:12 - Implement error handling for HTTP status codes and add retry logic for user registration in the database
> - **cae3995** 2025-02-14 10:50:39 - Refine risk assessment guidelines in get_ai_assessment_tips function: reduce required hazards from 5 to 3, clarify JSON response format, and emphasize focus on user's house.
> - **3c86666** 2025-02-13 13:00:26 - Create README.md
> - **ff805b1** 2025-02-13 09:40:13 - Increase bottom margin in forecast template for improved layout
> - **c5d2ec0** 2025-02-13 09:35:14 - Add user IP address handling: set IP in session and fetch location based on user IP
> - **5c405cd** 2025-02-12 09:44:36 - Update app.run configuration to specify host and port
> - **6feb167** 2025-02-12 09:38:32 - Refactor WSGI setup: remove old wsgi.py, create new wsgi.py for proper app import and host/port configuration
> - **8078383** 2025-02-12 09:33:54 - Add WSGI entry point with host and port configuration; update requirements to include Gunicorn
> - **4f5cdd1** 2025-02-12 09:09:29 - Refactor dashboard and tracker styles; adjust overflow behavior in forecast; update advice line limit in weather tips; add WSGI entry point
> - **f2a704e** 2025-02-12 00:09:35 - Enhance mood logging with error handling and user feedback; improve air quality average calculation documentation
> - **0b5f566** 2025-02-11 23:43:38 - Fix air quality index rounding and update documentation for database support
> - **92f2059** 2025-02-11 22:59:43 - Merge pull request #11 from 23knightst813/fix-tracker-page-1
> - **c6b2c8c** 2025-02-11 22:59:34 - Fix tracker page rendering issue
> - **14992ab** 2025-02-11 22:50:36 - Merge pull request #9 from 23knightst813/fix-tracker-page
> - **896ae1f** 2025-02-11 22:50:25 - Fix tracker page
> - **842889c** 2025-02-11 22:44:35 - Attempted to Add mood logging functionality and enhance weather data retrieval in tracker
> - **54e6f4e** 2025-02-11 21:39:26 - Refactor tracker layout and enhance styling for improved user experience
> - **3d9689b** 2025-02-10 16:14:58 - began to add tracker
> - **fc8f954** 2025-02-07 11:28:21 - Update dashboard layout and fix SQL query in weather module
> - **ece5d8c** 2025-02-07 10:46:19 - Merge branch 'main' of https://github.com/23knightst813/Health-Advice-Group
> - **fd122de** 2025-02-07 10:46:07 - Merge pull request #7 from 23knightst813/add-comments
> - **905b94d** 2025-02-07 10:44:03 - added changelog
> - **27097eb** 2025-02-07 10:43:57 - Add comments to Python, HTML, and JS files
> - **8860c19** 2025-02-07 10:25:05 - Finsihed the risk assessment funcitonalty
> - **ee9f70c** 2025-02-07 09:37:18 - Add risk assessment feature with form handling and database integration
> - **76dff77** 2025-02-04 15:06:28 - Refactor AQI categorization labels, enhance dashboard layout, and improve error handling messages
> - **9056520** 2025-02-04 13:20:32 - Refactor AQI categorization by importing function and removing redundant code; enhance error handling in dashboard
> - **2e9b278** 2025-02-04 13:19:20 - Update test log documentation with event details, expected and actual results for improved clarity
> - **f515f59** 2025-02-04 13:18:10 - Add AQI categorization, enhance dashboard image handling, and improve flash message visibility
> - **233a8d4** 2025-02-04 13:09:02 - Merge pull request #4 from 23knightst813/fix-data-parsing
> - **73afda4** 2025-02-04 13:08:51 - Fix data parsing in air quality dashboard
> - **1416414** 2025-02-04 13:06:16 - Enhance dashboard with dynamic air quality data and health recommendations; update styles and fix test log formatting ( broken )
> - **19b4871** 2025-02-04 11:50:09 - Refactor forecast template for improved styling; update AI tips generation requirements for clarity and detail
> - **919d3b0** 2025-02-04 11:39:54 - Update test log with new test cases and fix typos; add air quality dashboard test case
> - **13d8558** 2025-02-04 11:29:57 - Add visual dashboard route and template
> - **4fb31a4** 2025-02-03 13:09:17 - Add logout functionality and update session management; modify templates for session-based user display
> - **bfcb7ae** 2025-01-31 12:15:58 - Add user ID retrieval by email and integrate health conditions in AI tips generation; update registration options
> - **7929b1d** 2025-01-31 11:45:16 - Refactor forecast template for improved layout and styling; update health tips section and enhance data parsing logic
> - **350fe68** 2025-01-31 11:02:21 - Integrate Google Generative AI for health tips generation; refactor weather data retrieval and enhance error handling
> - **92dc1c4** 2025-01-31 09:33:56 - Add environment variable support and integrate Google Generative AI; update .gitignore and requirements
> - **7efd63c** 2025-01-31 09:24:48 - Enhance forecast display with improved styling and layout; fix CSS issues and capitalize location name
> - **c2c30ba** 2025-01-30 13:16:36 - Implement weather forecast feature with location-based data retrieval; add forecast template and styling
> - **529b691** 2025-01-30 09:41:49 - Refactor weather retrieval logic to use city name for geocoding; update API calls for location and weather data
> - **c20631f** 2025-01-30 09:18:06 - Add asset log documentation for libraries and resources used
> - **ea3830e** 2025-01-29 12:10:33 - started to add weather API logic and implement location retrieval based on IP address
> - **5dabccf** 2025-01-29 11:24:37 - Migrate requirements file to root directory; remove old requirements file from flaskr
> - **9df490e** 2025-01-29 09:44:07 - Fix weather API URL to use latitude and longitude parameters; update API key variable name
> - **efb83ac** 2025-01-29 09:43:36 - Add weather API integration and enhance database schema; update CRD field default value and create testing log
> - **34706e8** 2025-01-28 15:06:31 - Enhance user registration flow and error handling; update registration form action and add flash message styling
> - **d9d45a1** 2025-01-28 13:11:45 - Fix user registration logic and update password handling; correct SQL syntax for user table
> - **fbd8373** 2025-01-28 12:55:04 - Implement user registration and login functionality with validation; enhance database schema
> - **341d5d8** 2025-01-28 12:29:26 - Set up SQLite database and create users table; add .gitignore for database file
> - **e98543a** 2025-01-28 12:24:45 - Add registration page and update login template; enhance styles
> - **11196a8** 2025-01-28 10:49:35 -  create login template; remove register template
> - **91f4670** 2025-01-27 16:11:17 - Added Some Register Page Styling
> - **16ceb26** 2025-01-27 15:29:15 - Update base and index templates; add login/logout functionality and improve CSS styles
> - **6102c96** 2025-01-24 12:11:53 - Add zero to nine words array for time representation in script.js
> - **5185fe5** 2025-01-24 12:05:10 - Enhance index and base templates with navigation links and update image format; improve CSS styles for navigation and body background
> - **99859d4** 2025-01-24 11:41:49 - Added the clock system , complted the base.html added imagies and text to index
> - **1e67699** 2025-01-24 08:47:31 - initial commit: add Flask application structure with authentication, validation, and basic styling
