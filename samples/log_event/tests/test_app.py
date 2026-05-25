def test_log_issue_comment(client, load_fixture, mocker):
    mock_logger = mocker.patch("app.logger")
    issue_comment_created_event = load_fixture("issue_comment_created_event")

    resp = client.post(
        "/",
        json=issue_comment_created_event,
        headers={"Content-Type": "application/json", "X-Github-Event": "issue_comment"},
    )

    assert resp.status_code == 200

    mock_logger.info.assert_called_once_with("some comment")


def test_log_issue_body(client, load_fixture, mocker):
    mock_logger = mocker.patch("app.LogIssue.logger")
    issues_opened_event = load_fixture("issues_opened_event")

    resp = client.post(
        "/",
        json=issues_opened_event,
        headers={"Content-Type": "application/json", "X-Github-Event": "issues"},
    )

    assert resp.status_code == 200

    mock_logger.info.assert_called_once_with("some issue")
