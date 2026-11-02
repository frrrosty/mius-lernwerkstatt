from aufgabe import *

# Gekürzt nach dem Deploy-Workflow von Shutter Call
WORKFLOW = """name: Deploy
on: workflow_dispatch
jobs:
  bauen:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - name: Hochladen
        uses: r0adkll/upload-google-play@v1.1.3
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
      - uses: ./.github/eigene-aktion
      - uses: docker://alpine:3.20
"""


def test_findet_alle_uses():
    """pruefe_workflow() findet die vier Actions mit @"""
    assert len(pruefe_workflow(WORKFLOW)) == 4


def test_felder():
    """Zeile, Aktion, Ref und fest sind richtig"""
    erste = pruefe_workflow(WORKFLOW)[0]
    assert erste == {"zeile": 7, "aktion": "actions/checkout", "ref": "v4", "fest": False}


def test_mit_name_davor():
    """Auch «uses:» ohne Bindestrich, nach einem name:, wird gefunden"""
    zeilen = [r["zeile"] for r in pruefe_workflow(WORKFLOW)]
    assert 12 in zeilen


def test_hash_ist_fest():
    """Ein 40-stelliger Hash gilt als fest, der Kommentar gehört nicht zum Ref"""
    r = [x for x in pruefe_workflow(WORKFLOW) if x["fest"]]
    assert len(r) == 1 and r[0]["ref"] == "11bd71901bbe5b1630ceea73d27597364c9af683"


def test_kurzer_hash_ist_nicht_fest():
    """Ein gekürzter Hash gilt nicht als fest"""
    r = pruefe_workflow("      - uses: actions/checkout@11bd719")
    assert r[0]["fest"] is False


def test_riskant():
    """riskant() nennt jede ungesicherte Action einmal"""
    assert riskant(WORKFLOW) == ["actions/checkout", "actions/setup-node", "r0adkll/upload-google-play"]
