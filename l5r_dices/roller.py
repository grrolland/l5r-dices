import re
import click
import typer
from random import randrange
from rich import print
from typing_extensions import Annotated


class L5RDices:
    def __init__(self, roll: int, keep: int):
        self.roll = int(roll)
        self.keep = int(keep)

    def __repr__(self):
        return f"<L5RDices: value={self.roll}G{self.keep}>"


class DicesParser(click.ParamType):
    name = "DicesParser"
    reg  = re.compile(r'(\d+)G(\d+)')
    def convert(self, value, param, ctx):
        match = self.reg.search(value)
        if match and match.group(1) >= match.group(2):
            return L5RDices(match.group(1),match.group(2))
        else:
            print(f"dices {value} incorrect")
            return


def roll(
  dices:  Annotated[L5RDices, typer.Argument(click_type=DicesParser())],
  explode: Annotated[bool, typer.Option("--explode", "-x", help="explode 10")] = False,
  spec: Annotated[bool, typer.Option("--spec", "-s", help="reroll 1")] = False,
):
    rolls = []
    for i in range(dices.roll):
        rolls.append(roll_one_dice(explode, spec))
    ordered_rolls = sorted(rolls, key=lambda d: d['result'], reverse=True)
    result = 0
    for i in range(dices.keep):
        result += ordered_rolls[i]['result']
    print_result(ordered_rolls, result)

def roll_one_dice(explode, spec):
    dices = []
    dice = randrange(10) + 1
    dices.append(dice)
    while dice == 1 and spec:
        dice = randrange(10) + 1
        dices.append(dice)
    final_dice = dice
    while dice == 10 and explode:
        dice = randrange(10) + 1
        dices.append(dice)
        final_dice += dice
    return { 'result' : final_dice, 'details' : dices }

def print_result(rolls, result):
    for r in rolls:
        fr = '{: >3}'.format(r['result'])
        print(f":game_die: [bold green]{fr}[/bold green] -- {format_details(r['details'])}")
    tr = '{: >3}'.format(result)
    print(f":direct_hit: [bold red] {result}[/bold red]")

def format_details(details):
    s = '['
    for idx, d in enumerate(details):
        s += '{: >2}'.format(d)
        if d == 10 and idx < len(details) - 1 :
            s += ':boom:'
        if d == 1 and idx < len(details) - 1 :
            s += ':repeat:'
        if idx < len(details) - 1 :
            s += ', '
    s += ']'
    return s

