# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0]

### Changed
- `GITHUBAPP_SECRET` can now be set to `False` to skip verifying the signature of
the webhook payload.

- The `X-Hub-Signature-256` header is now preferred for signature checking.
Previously, `X-Hub-Signature` (and `sha1`) were used to verify the payload.

## [0.2.0]
### Added
- This changelog.
- Several new tests.

### Changed
- Response now includes whether any functions were called as the "status" as well
as a map of function names and returned values of any functions called as "calls"
(JSON formatted). Due to this functions must now return JSON serializable data.
The goal is to aid in debugging, as GitHub allows app owners to view hook responses.

## 0.1.0
### Added
- Initial release


[Unreleased]: https://github.com/bradshjg/flask-githubapp/compare/0.3.0...HEAD
[0.2.0]: https://github.com/bradshjg/flask-githubapp/compare/0.1.0...0.2.0
[0.3.0]: https://github.com/bradshjg/flask-githubapp/compare/0.2.0...0.3.0
