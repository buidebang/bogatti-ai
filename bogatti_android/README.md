# bogatti - Android Edition

This is the Android implementation of the bogatti project, featuring a Spotify-inspired UI/UX and modular configuration logic.

## Key Features
- **Spotify Style UI**: Dark theme (#000000), Spotify Green accents (#1DB954), and smooth transitions.
- **Modular Config**: Dynamic UI updates and API management via `ModularConfigManager`.
- **SSH/CLI Bridge**: Optimized query formatting for `gemini-cli` usage during internet outages.
- **Local Persistence**: Chat history stored using Room Database.
- **Vazirmatn Font**: Native support for Persian/RTL text.

## Project Structure
- `app/src/main/java/com.bogatti.ir/ui`: Jetpack Compose screens and themes.
- `app/src/main/java/com.bogatti.ir/service`: AI Service and Modular Logic.
- `app/src/main/java/com.bogatti.ir/data`: Persistence and Credit Management.

## Build Instructions
1. Open the project in Android Studio.
2. Place `vazirmatn_regular.ttf` and `vazirmatn_bold.ttf` in `app/src/main/res/font/`.
3. Sync Gradle and build the project.
4. The app uses Room and Jetpack Compose.
