# 📱 NirapodPoint — Frontend Setup Guide

**React Native · Expo SDK 54 · TypeScript · Zustand · React Navigation**

---

## 📋 Table of Contents

- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Step-by-Step Setup](#-step-by-step-setup)
- [Environment Variables](#-environment-variables)
- [Running on Devices](#-running-on-devices)
- [Project Structure](#-project-structure)
- [Key Screens & Components](#-key-screens--components)
- [State Management](#-state-management)
- [Running Tests](#-running-tests)
- [Building for Production](#-building-for-production)
- [Troubleshooting](#-troubleshooting)

---

## ✅ Prerequisites

| Tool | Version | Download |
|---|---|---|
| Node.js | 18 LTS or 20 LTS | https://nodejs.org |
| npm | 9+ (comes with Node) | — |
| Expo CLI | Latest (via npx) | No install needed |
| Android Studio | Latest | https://developer.android.com/studio *(for Android emulator)* |
| Xcode | 15+ | Mac App Store *(for iOS simulator — Mac only)* |
| Expo Go App | Latest | [Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent) / [App Store](https://apps.apple.com/app/expo-go/id982107779) *(for physical device)* |
| Git | Latest | https://git-scm.com |

> ⚠️ **Important:** The backend API must be running before you start the frontend. See [backend/README.md](../backend/README.md).

---

## ⚡ Quick Start

```bash
# 1. Navigate to the frontend directory
cd "NirapodPoint App/frontend"

# 2. Install dependencies
npm install

# 3. Configure environment
cp .env.example .env
# Edit .env — set API_BASE_URL to your backend address

# 4. Start Expo development server
npx expo start
```

Then choose your target:
- Press **`a`** → Android emulator
- Press **`i`** → iOS simulator *(Mac only)*
- **Scan QR code** → Expo Go on physical device

---

## 🛠️ Step-by-Step Setup

### STEP 1 — Install Node.js

Download Node.js **18 LTS** or **20 LTS** from https://nodejs.org

Verify installation:
```bash
node --version    # should print v18.x.x or v20.x.x
npm --version     # should print 9.x.x or higher
```

---

### STEP 2 — Clone the Repository

```bash
git clone https://github.com/ArafatBytes/Nirapod-Point-Mobile-App.git
cd "NirapodPoint App/frontend"
```

---

### STEP 3 — Install Dependencies

```bash
npm install
```

This installs all packages listed in `package.json`, including React Native, Expo, navigation, maps, camera, voice recognition, and all UI libraries.

> ⚠️ **Do not use `yarn`** — the project uses `npm`. Mixing package managers causes lock-file conflicts.

---

### STEP 4 — Configure Environment Variables

```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# Linux / Mac
cp .env.example .env
```

Open `.env` and set the following:

```env
# Point this to your running backend server
# For Android emulator: use 10.0.2.2 instead of localhost
API_BASE_URL=http://10.0.2.2:8000/api/v1

# For iOS simulator or physical device on same WiFi:
# API_BASE_URL=http://192.168.x.x:8000/api/v1
# (replace with your machine's local IP)

# Optional — Google Maps
GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here
```

> 💡 **Find your local IP:**
> ```bash
> # Windows
> ipconfig | findstr "IPv4"
> # Linux/Mac
> ifconfig | grep "inet "
> ```

---

### STEP 5 — Set Up an Emulator or Physical Device

#### Option A — Android Emulator (Android Studio)

1. Install **Android Studio**: https://developer.android.com/studio
2. Open Android Studio → **More Actions** → **Virtual Device Manager**
3. Click **Create Device** → choose **Pixel 7** (or any device)
4. Select **API Level 34** (Android 14) system image → Download if needed
5. Click **Finish** → Click the ▶️ Play button to start the emulator

#### Option B — iOS Simulator (Mac only)

1. Install **Xcode** from the Mac App Store
2. Open Xcode → **Settings** → **Platforms** → Download **iOS 17**
3. Run the simulator:
   ```bash
   open -a Simulator
   ```

#### Option C — Physical Device (Easiest)

1. Install **Expo Go** on your phone:
   - Android: [Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent)
   - iOS: [App Store](https://apps.apple.com/app/expo-go/id982107779)
2. Make sure your phone and computer are on the **same WiFi network**
3. Set `API_BASE_URL` in `.env` to your computer's local IP

---

### STEP 6 — Start the Expo Development Server

```bash
npx expo start
```

You'll see a screen like this:
```
› Metro waiting on exp://192.168.x.x:8081
› Scan the QR code above with Expo Go (Android) or the Camera app (iOS)
› Press a │ open Android
› Press i │ open iOS simulator
› Press w │ open web
```

Choose your target:
- **`a`** — opens the Android emulator
- **`i`** — opens the iOS simulator *(Mac only)*
- **Scan QR** — opens in Expo Go on your physical device

---

### STEP 7 — Verify the App is Connected to the Backend

1. Open the app → you should see the **Splash screen**, then the **Login/Register** screen
2. Register a new account
3. Log in — if you reach the **Home screen with a map**, everything is working ✅

---

## 🔑 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `API_BASE_URL` | ✅ | Backend API base URL (`http://10.0.2.2:8000/api/v1` for Android emulator) |
| `GOOGLE_MAPS_API_KEY` | ❌ | Google Maps API key (app uses OpenStreetMap as fallback) |

> **Android Emulator note:** Android emulator uses `10.0.2.2` to refer to the host machine's `localhost`. So if your backend is at `localhost:8000`, set `API_BASE_URL=http://10.0.2.2:8000/api/v1`.

> **Physical device note:** Use your computer's actual LAN IP (e.g., `http://192.168.1.5:8000/api/v1`). Both devices must be on the same WiFi.

---

## 📱 Running on Devices

### Android Emulator

```bash
npx expo start --android
# or press 'a' in the running Expo server
```

### iOS Simulator (Mac only)

```bash
npx expo start --ios
# or press 'i' in the running Expo server
```

### Physical Device

```bash
npx expo start
# Scan the QR code with Expo Go
```

### Tunnel Mode (different network)

If your phone and computer are on different networks:

```bash
npx expo start --tunnel
```

This creates a public tunnel URL. Requires: `npm install -g @expo/ngrok`

---

## 📂 Project Structure

```
frontend/
├── App.tsx                          # Root component (entry point)
├── index.js                         # Expo entry point
├── app.json                         # Expo configuration (app name, icons, etc.)
├── tsconfig.json                    # TypeScript configuration
├── babel.config.js                  # Babel transpiler config
├── metro.config.js                  # Metro bundler config
├── package.json                     # npm dependencies
│
├── src/
│   ├── navigation/                  # Screen navigation
│   │   ├── RootNavigator.tsx        # Root: chooses Auth or Main based on login state
│   │   ├── AuthNavigator.tsx        # Stack: Login → Register
│   │   └── MainTabNavigator.tsx     # Bottom tabs: Home, Map, Reports, Profile
│   │
│   ├── screens/
│   │   ├── Splash/
│   │   │   └── SplashScreen.tsx     # Initial loading screen
│   │   ├── Auth/
│   │   │   ├── LoginScreen.tsx      # Email + password login
│   │   │   └── RegisterScreen.tsx   # New account creation
│   │   ├── Home/
│   │   │   └── HomeScreen.tsx       # Dashboard: map overview + quick actions
│   │   ├── Map/
│   │   │   └── MapScreen.tsx        # Route planning + safety scores
│   │   ├── Reports/
│   │   │   ├── ReportsScreen.tsx    # List of crime reports
│   │   │   └── AddReportScreen.tsx  # Submit report + AI analysis display
│   │   └── Profile/
│   │       ├── ProfileScreen.tsx    # User info + settings
│   │       ├── ContactsScreen.tsx   # Emergency contact management
│   │       └── SOSConfigScreen.tsx  # SOS voice trigger configuration
│   │
│   ├── store/                       # Zustand global state
│   │   ├── authStore.ts             # User session: token, user object, login/logout
│   │   └── locationStore.ts         # Current GPS position, tracking status
│   │
│   ├── services/                    # API communication layer (axios)
│   │   ├── api.service.ts           # Base axios instance with auth headers
│   │   ├── auth.service.ts          # register(), login(), getMe()
│   │   ├── crime.service.ts         # submitReport(), analyzeImage()
│   │   ├── route.service.ts         # calculateRoutes()
│   │   └── sos.service.ts           # triggerSOS()
│   │
│   ├── hooks/                       # Custom React hooks
│   │   ├── useLocation.ts           # GPS tracking with background support
│   │   ├── useVoiceActivation.ts    # "NirapodPoint Emergency" detection
│   │   └── useSafeRoute.ts          # Route state management
│   │
│   ├── components/                  # Reusable UI components
│   │   ├── SafeRouteCard.tsx        # Displays a single route with safety badge
│   │   ├── CrimeReportCard.tsx      # Compact crime report display
│   │   ├── SOSButton.tsx            # Large red SOS trigger button
│   │   └── LoadingOverlay.tsx       # Full-screen spinner
│   │
│   ├── types/                       # TypeScript interface definitions
│   │   ├── auth.types.ts
│   │   ├── crime.types.ts
│   │   └── route.types.ts
│   │
│   ├── theme/                       # Design system
│   │   └── index.ts                 # Colors, typography, spacing constants
│   │
│   ├── constants/
│   │   └── index.ts                 # App-wide constants (API URL, timeouts)
│   │
│   └── utils/                       # Helper functions
│       ├── formatters.ts            # Date, distance, score formatting
│       └── permissions.ts           # Camera, location permission helpers
│
├── assets/                          # Static assets
│   ├── images/                      # App images and icons
│   └── sounds/                      # SOS alert sounds
│
├── android/                         # Android native project files
└── ios/                             # iOS native project files
```

---

## 🖥️ Key Screens & Components

### Login / Register
Standard form screens using `react-hook-form` + `yup` for validation. On successful login, the JWT token is stored in `authStore` and `expo-secure-store`.

### Home Screen
Displays the map (`react-native-maps`) centered on the user's current location. Shows nearby crime reports as map markers. Background GPS tracking starts automatically.

### Map & Route Screen
- User inputs source and destination (address search)
- Calls `POST /api/v1/routes/calculate`
- Displays 3 route options: Optimal, Safest, Fastest
- Each route shows distance, duration, and safety score badge (0–100, colour-coded)

### Add Report Screen
- Select crime category and severity
- Pick or take a photo (via `expo-image-picker`)
- Photo is sent to backend → AI analysis runs automatically
- Result displayed: detected objects, crime type, confidence, AI-generated title and description

### SOS Emergency
- Voice activation: say **"NirapodPoint Emergency"** (detected via `@react-native-voice/voice`)
- Camera starts recording (via `expo-camera`)
- Video + location sent to `POST /api/v1/sos/trigger`
- Confirmation screen shows contacts notified

---

## 🗄️ State Management

The app uses **Zustand** for lightweight global state.

### `authStore`

```typescript
{
  token: string | null       // JWT access token
  user: User | null          // Logged-in user object
  setAuth(token, user): void // Called after login
  logout(): void             // Clears token + user
}
```

### `locationStore`

```typescript
{
  currentLocation: Coordinates | null   // Latest GPS fix
  isTracking: boolean                   // Background tracking active?
  setLocation(coords): void
  startTracking(): void
  stopTracking(): void
}
```

---

## 🧪 Running Tests

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run a specific test file
npm test -- AddReportScreen.test.tsx

# Watch mode (re-runs on file change)
npm test -- --watchAll
```

---

## 🏗️ Building for Production

### Android APK (for testing)

```bash
npx expo build:android --type apk
```

### Android AAB (for Play Store)

```bash
npx expo build:android --type app-bundle
```

### iOS IPA (requires Mac + Apple Developer account)

```bash
npx expo build:ios
```

### Using EAS Build (recommended)

```bash
# Install EAS CLI
npm install -g eas-cli

# Login to Expo account
eas login

# Configure build
eas build:configure

# Build for Android
eas build --platform android

# Build for iOS
eas build --platform ios
```

---

## 🔍 Troubleshooting

### ❌ `npm install` fails with permission errors

```bash
# Windows — run PowerShell as Administrator
# Linux/Mac — do NOT use sudo with npm
npm install --legacy-peer-deps
```

---

### ❌ Metro bundler can't connect / QR code won't scan

1. Make sure your phone and computer are on the **same WiFi network**
2. Try tunnel mode: `npx expo start --tunnel`
3. Clear Metro cache: `npx expo start --clear`

---

### ❌ App shows "Network Error" when calling the backend

Check `API_BASE_URL` in `.env`:

| Device | Correct URL |
|---|---|
| Android Emulator | `http://10.0.2.2:8000/api/v1` |
| iOS Simulator | `http://localhost:8000/api/v1` |
| Physical device (same WiFi) | `http://192.168.x.x:8000/api/v1` |

---

### ❌ Maps not showing (blank white screen)

This is usually a missing Google Maps API key.

1. Go to https://console.cloud.google.com
2. Enable **Maps SDK for Android** and **Maps SDK for iOS**
3. Create an API key
4. Add to `.env`: `GOOGLE_MAPS_API_KEY=your_key`

---

### ❌ Camera or location permission denied

The app requests permissions at runtime. If denied:
1. Go to device **Settings → Apps → NirapodPoint**
2. Enable **Camera**, **Microphone**, and **Location** permissions manually

---

### ❌ `expo: command not found`

Use `npx expo` instead of `expo`:
```bash
npx expo start
```

---

### ❌ Build fails with `Could not find the following Gradle modules`

```bash
cd android
./gradlew clean    # Linux/Mac
gradlew.bat clean  # Windows
cd ..
npx expo start
```

---

### ❌ TypeScript errors during development

```bash
# Check types without running
npx tsc --noEmit

# Fix auto-fixable lint issues
npm run lint -- --fix
```

---

## 🔧 Useful Scripts

```bash
# Start Expo server
npx expo start

# Start with cleared cache
npx expo start --clear

# Type-check the project
npx tsc --noEmit

# Lint the project
npm run lint

# Run tests
npm test

# Install a new package (use this instead of npm install to keep Expo compatible)
npx expo install <package-name>
```

> ⚠️ **Always use `npx expo install`** (not plain `npm install`) when adding new packages — it ensures the package version is compatible with your Expo SDK version.

---

*NirapodPoint Frontend — Islamic University of Technology, CSE 4510*
