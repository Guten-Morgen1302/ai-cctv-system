# Contributing to SecureVista

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/ai-cctv-system.git`
3. Create a branch: `git checkout -b feature/your-feature`
4. Set up environment: `python -m venv venv && source venv/bin/activate`
5. Install deps: `pip install -r requirements.txt`

## Code Style

- Follow PEP 8 guidelines
- Use type hints where applicable
- Add docstrings to all functions
- Keep functions focused and small

## Commit Guidelines

- Use conventional commits: `type: description`
- Types: feat, fix, docs, perf, refactor, test, ci
- Example: `feat: add loitering detection algorithm`

## Testing

- Run tests: `python -m pytest tests/`
- Aim for 80%+ coverage
- Test both happy and error paths

## Pull Request Process

1. Create feature branch
2. Commit changes with clear messages
3. Push to your fork
4. Create PR with description
5. Address review comments
6. Squash commits if requested

## Areas for Contribution

- [ ] Additional ML models
- [ ] Mobile app integration
- [ ] Database optimization
- [ ] Frontend improvements
- [ ] Documentation
- [ ] Bug fixes

## Questions?

Create an issue or contact: dev@securevista.dev
