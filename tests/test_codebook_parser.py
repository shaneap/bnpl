import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from codebook import is_rule, parse_lines  # noqa: E402

RULE = "-" * 84

# Two layouts seen in the SHED codebooks: 2021 (lowercase fields, two-space header) and
# 2022+ (tabs, capitalized fields, single-space header, broken rules).
LAYOUT_2021 = f"""{RULE}
BNPL3                                  In the past year, have you ever been late
                                       making a payment for something you bought
                                       using a Buy Now Pay Later service?
{RULE}
                  type:  numeric (byte)
                 label:  BNPL3
         unique values:  2                        missing .:  10,767/11,874
            tabulation:        Freq.     Numeric    Label
                           948                  0   No
                           159                  1   Yes
                        10,767                  .
{RULE}"""

LAYOUT_2022 = f"""{RULE}
B3A_d You have more debt          - You said that you (and
                                       your family) are somewhat worse off
{"-" * 24}      {"-" * 60}
                      Type: Numeric (byte)
           Unique values: 2                         Missing .: 9,322/12,934
                        Freq.   Numeric  Label Tabulation:
                              5,349         0  Never carried an unpaid balance
                                                   (always pay in full)
                                576         1  Once
{RULE}"""


def lines(text):
    return [(1, l.expandtabs()) for l in text.splitlines()]


def test_rule_detection():
    assert is_rule(RULE)
    assert is_rule("-" * 24 + "      " + "-" * 60)
    assert not is_rule("BNPL3   In the past year")


def test_parse_2021_layout():
    v = parse_lines(lines(LAYOUT_2021))["BNPL3"]
    assert v.label.startswith("In the past year, have you ever been late making a payment")
    assert v.label.endswith("Buy Now Pay Later service?")
    assert (v.missing, v.total, v.nonmissing) == (10767, 11874, 1107)
    assert [(c, l) for _, c, l in v.codes] == [("0", "No"), ("1", "Yes"), (".", "")]


def test_parse_2022_layout_single_space_header_and_wrapped_codes():
    v = parse_lines(lines(LAYOUT_2022))["B3A_d"]
    assert v.label.startswith("You have more debt - You said")
    assert v.missing == 9322
    assert v.codes[0][2] == "Never carried an unpaid balance (always pay in full)"
