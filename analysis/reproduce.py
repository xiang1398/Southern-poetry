#!/usr/bin/env python3
"""Reproduce Southern Poetry exploratory tone tables from verse_lines.tsv.

Uses Python standard library only. 4-tone ambiguity is excluded from strict
tables; P/Z allows multiple readings only when all belong to one binary class.
Dynasty labels are AUTHOR COHORT PROXIES, not poem-level composition dates.
"""
import csv
import json
import math
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
TONES = "平上去入"
BINARY = "PZ"


def load_lines():
    with (HERE / "verse_lines.tsv").open(encoding="utf-8", newline="") as f:
        lines = list(csv.DictReader(f, delimiter="\t"))
    for line in lines:
        n = int(line["line_length"])
        assert n in (5, 7)
        assert len(line["tones_binary"]) == n
        assert len(line["tones_strict"]) == n
    return lines


def pair(lines, i, j, mode="binary"):
    alphabet = BINARY if mode == "binary" else TONES
    field = "tones_binary" if mode == "binary" else "tones_strict"
    subset = [r for r in lines if int(r["line_length"]) > max(i, j)]
    table = Counter()
    for row in subset:
        a, b = row[field][i], row[field][j]
        if a in alphabet and b in alphabet:
            table[a + b] += 1
    n = sum(table.values())
    m1 = {t: sum(table[t + u] for u in alphabet) for t in alphabet}
    m2 = {t: sum(table[u + t] for u in alphabet) for t in alphabet}
    if mode == "binary":
        observed = table["PZ"] + table["ZP"]
        expected = ((m1["P"] * m2["Z"] + m1["Z"] * m2["P"]) / n) if n else 0
    else:
        observed = n - sum(table[t + t] for t in alphabet)
        expected = n - sum(m1[t] * m2[t] / n for t in alphabet) if n else 0
    answer = {
        "n": n,
        "possible_lines": len(subset),
        "observed": observed,
        "observed_rate": observed / n if n else None,
        "expected_independent": expected,
        "expected_rate": expected / n if n else None,
        "excess_percentage_points": 100 * (observed - expected) / n if n else None,
        "table": dict(sorted(table.items())),
    }
    if mode == "four":
        zz = sum(table[a + b] for a in "上去入" for b in "上去入")
        dif = sum(table[a + b] for a in "上去入" for b in "上去入" if a != b)
        z2, z4 = sum(m1[a] for a in "上去入"), sum(m2[a] for a in "上去入")
        expected_zz_diff = (
            1 - sum(m1[t] / z2 * m2[t] / z4 for t in "上去入")
            if zz and z2 and z4 else None
        )
        answer["within_ZZ"] = {
            "n": zz,
            "different": dif,
            "rate": dif / zz if zz else None,
            "expected_independent_rate": expected_zz_diff,
        }
    return answer


def triple(lines):
    subset = [
        r for r in lines
        if int(r["line_length"]) == 7
        and all(r["tones_binary"][i] in BINARY for i in (1, 3, 5))
    ]
    patterns = Counter("".join(r["tones_binary"][i] for i in (1, 3, 5))
                       for r in subset)
    n = len(subset)
    margins = [
        sum(r["tones_binary"][i] == "P" for r in subset) / n if n else 0
        for i in (1, 3, 5)
    ]
    expected = (margins[0] * (1 - margins[1]) * margins[2]
                + (1 - margins[0]) * margins[1] * (1 - margins[2]))
    return {
        "n": n, "PZP": patterns["PZP"], "ZPZ": patterns["ZPZ"],
        "alternating_rate": (patterns["PZP"] + patterns["ZPZ"]) / n if n else None,
        "expected_independent_rate": expected if n else None,
    }


def gaussian_solve(a, b):
    n = len(b)
    m = [list(a[i]) + [b[i]] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(m[r][col]))
        m[col], m[pivot] = m[pivot], m[col]
        if abs(m[col][col]) < 1e-12:
            return None
        v = m[col][col]
        for j in range(col, n + 1):
            m[col][j] /= v
        for r in range(n):
            if r == col:
                continue
            v = m[r][col]
            for j in range(col, n + 1):
                m[r][j] -= v * m[col][j]
    return [row[n] for row in m]


def loglinear_fit(table, effects):
    observations = []
    for i, first in enumerate(TONES):
        for j, second in enumerate(TONES):
            x = [1] + [int(i == k) for k in (1, 2, 3)] \
                    + [int(j == k) for k in (1, 2, 3)]
            if "binary" in effects:
                x.append(int((i == 0) != (j == 0)))
            if "four" in effects:
                x.append(int(i != j))
            observations.append((table.get(first + second, 0), x))
    k = len(observations[0][1])
    params = [0.0] * k
    params[0] = math.log(max(1, sum(y for y, _ in observations)) / 16)

    def loglike(beta):
        result = 0.0
        for count, row in observations:
            eta = sum(v * b for v, b in zip(row, beta))
            if eta > 700:
                return float("-inf")
            result += count * eta - math.exp(eta)
        return result

    old = loglike(params)
    for _ in range(100):
        gradient = [0.0] * k
        information = [[0.0] * k for _ in range(k)]
        for count, x in observations:
            mu = math.exp(sum(v * b for v, b in zip(x, params)))
            for i in range(k):
                gradient[i] += x[i] * (count - mu)
                for j in range(k):
                    information[i][j] += mu * x[i] * x[j]
        for i in range(k):
            information[i][i] += 1e-9
        increment = gaussian_solve(information, gradient)
        if increment is None:
            break
        scale = 1.0
        while scale > 1e-8:
            candidate = [b + scale * v for b, v in zip(params, increment)]
            now = loglike(candidate)
            if now >= old - 1e-7:
                break
            scale /= 2
        params = candidate
        if abs(now - old) < 1e-8:
            old = now
            break
        old = now
    return {"AIC": 2 * k - 2 * old, "log_likelihood_without_constant": old}


def analyze():
    lines = load_lines()
    groups = {"all": lines}
    for era in ("宋", "齊", "梁", "陳", "未定"):
        groups[era] = [r for r in lines if r["author_cohort"] == era]
    result = {}
    for era, rows in groups.items():
        five = [r for r in rows if r["line_length"] == "5"]
        seven = [r for r in rows if r["line_length"] == "7"]
        four = pair(five, 1, 3, "four")
        model_aic = {
            key: loglinear_fit(four["table"], effects)["AIC"]
            for key, effects in (
                ("independent", ()), ("binary", ("binary",)),
                ("four", ("four",)), ("both", ("binary", "four")),
            )
        } if four["n"] else {}
        result[era] = {
            "five_lines": len(five), "seven_lines": len(seven),
            "2_4_binary": pair(five, 1, 3, "binary"),
            "2_4_four": four,
            "3_5_binary": pair(five, 2, 4, "binary"),
            "3_5_four": pair(five, 2, 4, "four"),
            "2_5_binary": pair(five, 1, 4, "binary"),
            "2_5_four": pair(five, 1, 4, "four"),
            "2_4_6_seven": triple(seven),
            "model_AIC": model_aic,
        }
    return result


if __name__ == "__main__":
    print(json.dumps(analyze(), ensure_ascii=False, indent=2))
