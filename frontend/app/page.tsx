import Link from 'next/link'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            Injury Risk Predictor
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Predict your injury risk using sports science research and machine learning.
            Based on the Acute:Chronic Workload Ratio (ACWR) methodology.
          </p>
          <Link
            href="/predict"
            className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            Get Started
          </Link>
        </div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 mb-16">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-2xl font-bold mb-3">Science-Based</h2>
            <p className="text-gray-600">
              Built on peer-reviewed research from sports science, using ACWR methodology
              established by Gabbett (2016).
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-2xl font-bold mb-3">ML-Powered</h2>
            <p className="text-gray-600">
              Machine learning models trained on training patterns to identify
              injury risk factors beyond simple thresholds.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-2xl font-bold mb-3">Actionable Insights</h2>
            <p className="text-gray-600">
              Get personalized recommendations to reduce injury risk and optimize
              your training load.
            </p>
          </div>
        </div>

        {/* What is ACWR Section */}
        <div className="bg-white p-8 rounded-lg shadow-md max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold mb-4">What is ACWR?</h2>
          <p className="text-gray-700 mb-4">
            The Acute:Chronic Workload Ratio (ACWR) is a key metric in sports science
            that predicts injury risk by comparing your recent training load (last 7 days)
            to your baseline fitness level (last 28 days average).
          </p>
          <div className="grid md:grid-cols-3 gap-4 mt-6">
            <div className="bg-green-50 p-4 rounded">
              <div className="font-bold text-green-800 mb-2">Low Risk (0.8-1.3)</div>
              <div className="text-sm text-green-700">Optimal training zone</div>
            </div>
            <div className="bg-yellow-50 p-4 rounded">
              <div className="font-bold text-yellow-800 mb-2">Moderate Risk (1.3-1.5)</div>
              <div className="text-sm text-yellow-700">Monitor closely</div>
            </div>
            <div className="bg-red-50 p-4 rounded">
              <div className="font-bold text-red-800 mb-2">High Risk (&gt;1.5)</div>
              <div className="text-sm text-red-700">Reduce training load</div>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
