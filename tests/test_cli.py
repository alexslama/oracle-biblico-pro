from shamir.cli import build_parser, command_doctor


def test_cli_parser_accepts_analyze_command():
    args = build_parser().parse_args(["analyze", "test question"])
    assert args.command == "analyze"
    assert args.query == "test question"


def test_doctor_runs_without_external_services(capsys):
    assert command_doctor(build_parser().parse_args(["doctor"])) == 0
    output = capsys.readouterr().out
    assert '"ready_for_base_mode": true' in output
