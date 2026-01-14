# Injury Risk Predictor - Frontend

Next.js frontend for the Injury Risk Predictor application.

## Setup

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Set API URL (optional):**
Create `.env.local` file (or use default localhost:8000):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. **Run development server:**
```bash
npm run dev
```

4. **Open browser:**
Visit http://localhost:3000

**Note:** Make sure the backend API is running on port 8000!

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── page.tsx           # Landing/dashboard page
│   ├── predict/
│   │   └── page.tsx      # Prediction form
│   ├── results/
│   │   └── page.tsx      # Prediction results
│   └── layout.tsx        # Root layout
├── components/            # React components
│   ├── TrainingLogForm.tsx
│   ├── RiskGauge.tsx
│   ├── ACWRChart.tsx
│   └── ...
├── lib/                   # Utilities
│   ├── api.ts            # API client
│   └── types.ts          # TypeScript types
└── public/               # Static assets
```

## Tech Stack

- **Next.js 14+** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Recharts** - Data visualization
- **Axios** - HTTP client
- **Zod** - Schema validation
