import { useState, useRef } from 'react'
import axios from 'axios'

const API_BASE = 'http://localhost:8000'

const EXAMPLE_QUERIES = [
  'Latest breakthroughs in quantum computing',
  'How does CRISPR gene editing work?',
  'The future of renewable energy',
  'Effects of social media on mental health',
]

const AGENT_STEPS = [
  { id: 'search',  icon: '🔍', label: 'Web Search Agent',       desc: 'Searching DuckDuckGo for relevant sources...' },
  { id: 'sum',     icon: '🧠', label: 'Summarisation Agent',     desc: 'Claude is synthesizing findings...' },
  { id: 'cite',    icon: '📚', label: 'Citation Agent',          desc: 'Formatting APA citations...' },
  { id: 'compile', icon: '📝', label: 'Orchestrator (LangGraph)', desc: 'Compiling final report...' },
]

export default function App() {
  const [query, setQuery]           = useState('')
  const [loading, setLoading]       = useState(false)
  const [activeStep, setActiveStep] = useState(-1)
  const [result, setResult]         = useState(null)
  const [error, setError]           = useState(null)
  const [showReport, setShowReport] = useState(false)
  const inputRef = useRef(null)

  async function handleSearch(e) {
    e.preventDefault()
    const q = query.trim()
    if (!q) return

    setLoading(true)
    setResult(null)
    setError(null)
    setShowReport(false)
    setActiveStep(0)

    // Simulate step progression for UX while the pipeline runs
    const stepTimings = [0, 1800, 4000, 6500]
    stepTimings.forEach((delay, i) => {
      setTimeout(() => {
        if (i < AGENT_STEPS.length) setActiveStep(i)
      }, delay)
    })

    try {
      const response = await axios.post(`${API_BASE}/research`, { query: q }, {
        timeout: 90000,
      })
      setResult(response.data)
      setActiveStep(AGENT_STEPS.length) // all done
    } catch (err) {
      const msg =
        err.response?.data?.detail ||
        err.message ||
        'An unexpected error occurred.'
      setError(msg)
      setActiveStep(-1)
    } finally {
      setLoading(false)
    }
  }

  function handleExampleClick(q) {
    setQuery(q)
    inputRef.current?.focus()
  }

  return (
    <div className="app">
      {/* ── Header ── */}
      <header className="header">
        <div className="container">
          <div className="header-badge">
            <span className="header-badge-dot" />
            Multi-Agent AI System
          </div>
          <h1>Research Assistant</h1>
          <p>
            Autonomous AI pipeline powered by LangGraph, Claude API, and real-time
            web search — delivering structured research reports in seconds.
          </p>
          <div className="agent-pills">
            <span className="agent-pill search">🔍 DuckDuckGo Search</span>
            <span className="agent-pill claude">🧠 Claude API</span>
            <span className="agent-pill cite">📚 APA Citations</span>
            <span className="agent-pill graph">⚡ LangGraph</span>
          </div>
        </div>
      </header>

      {/* ── Main ── */}
      <main style={{ flex: 1 }}>
        <div className="container">

          {/* Search */}
          <section className="search-section">
            <form className="search-form" onSubmit={handleSearch}>
              <div className="search-input-wrapper">
                <span className="search-icon">🔍</span>
                <input
                  ref={inputRef}
                  className="search-input"
                  type="text"
                  placeholder="Ask a research question…"
                  value={query}
                  onChange={e => setQuery(e.target.value)}
                  disabled={loading}
                />
              </div>
              <button className="search-btn" type="submit" disabled={loading || !query.trim()}>
                {loading ? (
                  <>
                    <span className="spinner" style={{ borderTopColor: '#fff' }} />
                    Researching…
                  </>
                ) : (
                  <>⚡ Research</>
                )}
              </button>
            </form>
          </section>

          {/* Loading state */}
          {loading && (
            <section className="loading-section">
              <div className="loading-agents">
                {AGENT_STEPS.map((step, i) => {
                  const isDone   = i < activeStep
                  const isActive = i === activeStep
                  return (
                    <div
                      key={step.id}
                      className={`loading-agent ${isActive ? 'active' : ''} ${isDone ? 'done' : ''}`}
                    >
                      <span className="agent-icon">{step.icon}</span>
                      <div style={{ flex: 1 }}>
                        <div style={{ fontWeight: 600, fontSize: 14 }}>{step.label}</div>
                        <div style={{ fontSize: 12, marginTop: 2 }}>
                          {isDone ? 'Complete' : isActive ? step.desc : 'Waiting…'}
                        </div>
                      </div>
                      {isDone   && <span style={{ fontSize: 18 }}>✅</span>}
                      {isActive && <span className="spinner" />}
                    </div>
                  )
                })}
              </div>
              <p className="loading-text">Running multi-agent pipeline…</p>
            </section>
          )}

          {/* Error */}
          {error && !loading && (
            <div className="error-card fade-in-up">
              <span className="error-icon">⚠️</span>
              <div className="error-body">
                <h4>Pipeline Error</h4>
                <p>{error}</p>
              </div>
            </div>
          )}

          {/* Results */}
          {result && !loading && (
            <section className="results-section fade-in-up">
              <div className="results-header">
                <h2>Research Report</h2>
                <span className="results-query" title={result.query}>{result.query}</span>
              </div>

              <div className="section-grid">
                {/* Overview */}
                {result.sections?.overview && (
                  <div className="card card-overview fade-in-up">
                    <div className="card-header">
                      <span className="card-icon">🌐</span>
                      <span className="card-title">Overview</span>
                    </div>
                    <p>{result.sections.overview}</p>
                  </div>
                )}

                {/* Key Findings */}
                {result.sections?.key_findings?.length > 0 && (
                  <div className="card fade-in-up">
                    <div className="card-header">
                      <span className="card-icon">🔑</span>
                      <span className="card-title">Key Findings</span>
                    </div>
                    <ul className="findings-list">
                      {result.sections.key_findings.map((finding, i) => (
                        <li key={i} className="finding-item">
                          <span className="finding-bullet" />
                          {finding}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Implications */}
                {result.sections?.implications && (
                  <div className="card card-implications fade-in-up">
                    <div className="card-header">
                      <span className="card-icon">💡</span>
                      <span className="card-title">Implications</span>
                    </div>
                    <p>{result.sections.implications}</p>
                  </div>
                )}
              </div>

              {/* Citations */}
              {result.citations?.length > 0 && (
                <div className="citations-section fade-in-up">
                  <h3>📚 Sources &amp; Citations</h3>
                  <div className="citations-list">
                    {result.citations.map(cite => (
                      <div key={cite.id} className="citation-card">
                        <div className="citation-num">{cite.id}</div>
                        <div className="citation-body">
                          <div className="citation-title">{cite.title}</div>
                          <div className="citation-apa">{cite.apa}</div>
                          <a
                            className="citation-link"
                            href={cite.url}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            {cite.url}
                          </a>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Full report toggle */}
              {result.report && (
                <div className="report-section fade-in-up">
                  <button
                    className="report-toggle"
                    onClick={() => setShowReport(v => !v)}
                  >
                    <span>📄 {showReport ? 'Hide' : 'View'} Full Markdown Report</span>
                    <span>{showReport ? '▲' : '▼'}</span>
                  </button>
                  {showReport && (
                    <div className="report-content">
                      <pre className="report-pre">{result.report}</pre>
                    </div>
                  )}
                </div>
              )}
            </section>
          )}

          {/* Empty state */}
          {!loading && !result && !error && (
            <div className="empty-state">
              <span className="empty-icon">🔬</span>
              <h3>Ready to research anything</h3>
              <p>
                Type a question above and the multi-agent pipeline will search the web,
                synthesize findings with Claude, and format proper citations.
              </p>
              <div className="example-queries">
                {EXAMPLE_QUERIES.map(q => (
                  <button
                    key={q}
                    className="example-query"
                    onClick={() => handleExampleClick(q)}
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}

        </div>
      </main>

      {/* ── Footer ── */}
      <footer className="footer">
        <div className="container">
          Built with{' '}
          <a href="https://www.langchain.com/langgraph" target="_blank" rel="noopener noreferrer">LangGraph</a>
          {' · '}
          <a href="https://www.anthropic.com" target="_blank" rel="noopener noreferrer">Claude API</a>
          {' · '}
          <a href="https://fastapi.tiangolo.com" target="_blank" rel="noopener noreferrer">FastAPI</a>
          {' · '}
          <a href="https://vitejs.dev" target="_blank" rel="noopener noreferrer">Vite + React</a>
        </div>
      </footer>
    </div>
  )
}
