from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)
WX_KEY = os.environ.get("WX_WEBHOOK_KEY", "")


def build_markdown(alerts):
    lines = []
    for a in alerts:
        status = "🔥 触发" if a.get("status") == "firing" else "✅ 恢复"
        labels = a.get("labels", {})
        ann = a.get("annotations", {})
        lines.append(f"### {status} {labels.get('alertname', '')}")
        if ann.get("summary"):
            lines.append(f"> {ann['summary']}")
        if ann.get("description"):
            lines.append(f"> {ann['description']}")
        svc = labels.get("service", labels.get("job", ""))
        if svc:
            lines.append(f"> 服务: `{svc}`")
        lines.append("---")
    return "\n".join(lines) or "Alertmanager 告警（无内容）"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True) or {}
    markdown = build_markdown(data.get("alerts", []))
    key = WX_KEY
    if not key:
        return jsonify({"error": "missing WX_WEBHOOK_KEY"}), 500
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"
    resp = requests.post(
        url,
        json={"msgtype": "markdown", "markdown": {"content": markdown}},
        timeout=10,
    )
    return (resp.text, resp.status_code)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
