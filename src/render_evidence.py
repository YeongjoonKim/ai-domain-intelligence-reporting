"""실제 공개 예제 출력을 HTML 검토 문서로 렌더링한다. 관리자 서비스가 아니다."""
import html
import json
from .export_evidence import build


def block(key, title, explanation, content):
    return ('<section id="' + key + '"><p class="scope">EXECUTED PUBLIC SAMPLE · SYNTHETIC</p>'
            + '<h2>' + html.escape(title) + '</h2><p>' + html.escape(explanation) + '</p>'
            + content + '<p class="limit">운영 데이터·실시간 API·모델 성능의 증거가 아닙니다.</p></section>')


def pre(value):
    text = value if isinstance(value, str) else json.dumps(value, indent=2, ensure_ascii=False)
    return "<pre>" + html.escape(text) + "</pre>"


def render():
    data = build()
    headers = ["id", "item", "metric", "unit", "period", "value"]
    rows = "<tr>" + "".join("<th>" + h + "</th>" for h in headers) + "</tr>"
    for row in data["observations"]:
        rows += "<tr>" + "".join("<td>" + html.escape(str(row[h])) + "</td>" for h in headers) + "</tr>"
    sections = block("inputs", "Observation contract", "합성 입력의 출처 ID·단위·시점을 보존합니다.", "<table>" + rows + "</table>")
    cards = ""
    for row in data["analysis"]["insights"]:
        cards += "<article><h3>" + html.escape(row["item"]) + "</h3>" + pre(row) + "</article>"
    sections += block("analysis", "Domain analysis", "단위별 비교와 부족한 이력을 구분한 실제 계산 결과입니다.", '<div class="cards">' + cards + "</div>")
    sections += block("report", "Generated evidence-linked brief", "템플릿으로 생성한 Markdown 보고서입니다. LLM이 작성한 문장으로 표시하지 않습니다.", pre(data["markdown"]))

    return ('<!doctype html><html lang="ko"><meta charset="utf-8">'
            + '<meta name="viewport" content="width=device-width, initial-scale=1">'
            + '<meta http-equiv="Content-Security-Policy" content="default-src &apos;none&apos;; style-src &apos;unsafe-inline&apos;; base-uri &apos;none&apos;; form-action &apos;none&apos;">'
            + '<title>Domain Intelligence · Execution Evidence</title>'
            + '<style>body{margin:0;background:#eff3f7;color:#183349;font:16px system-ui,sans-serif}'
            + 'main{max-width:1160px;margin:30px auto;padding:0 24px}section{background:white;padding:28px;margin:24px 0;border:1px solid #cbd5df;border-radius:12px}'
            + 'h1{font-size:28px}h2{font-size:25px}.scope{color:#147863;font-size:12px;font-weight:700;letter-spacing:1px}'
            + '.limit{font-size:13px;color:#546478}pre{font:14px/1.5 monospace;white-space:pre-wrap;overflow-wrap:anywhere}'
            + '.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}article{padding:15px;background:#f3f6f9;border-radius:8px}'
            + 'table{width:100%;border-collapse:collapse}td,th{padding:12px 6px;text-align:left;border-bottom:1px solid #d8e0e8;font-size:13px}'
            + '@media(max-width:700px){.cards{grid-template-columns:1fr}table{display:block;overflow:auto}}</style>'
            + '<main><h1>Domain Intelligence · Execution Evidence</h1>'
            + '<p>Reconstructed Public Example · Python 실행 결과를 렌더링한 검토 문서</p>'
            + sections + '</main></html>')


if __name__ == "__main__":
    print(render())
