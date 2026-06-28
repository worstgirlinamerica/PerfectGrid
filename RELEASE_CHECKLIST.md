# Release Checklist

1. Update `APP_VERSION` in `app.py`.
2. Update `CHANGELOG.md`.
3. Commit changes.
4. Push `main`.
5. Confirm the GitHub Actions build passes.
6. Tag the release:

```bash
git tag v1.0.0
git push origin v1.0.0
```

7. Check the generated GitHub Release and download both zip files.
8. Test the Windows zip on a Windows machine before sharing widely.

