from __future__ import division, print_function
import click
from terminaltables import AsciiTable

def frange(x, y, step):
    while x < y:
         yield x
         x += step

def option(*args, **kwargs):
    prompt = kwargs.pop('prompt', True)
    return click.option(*args, **kwargs, prompt=prompt)

def tabled(headers, rows):
    return AsciiTable(
        [headers] +
        [[round(c, 6) if isinstance(c, float) else c for c in r] for r in rows]
    )

@click.group()
@option('--dydx', prompt='dy/dx')
@option('--x0', type=float)
@option('--y0', type=float)
@option('--to_x', type=float, prompt='Ending X')
@option('--step', type=float)
@click.pass_context
def cli(ctx, **kwargs):
    ctx.args = kwargs

@cli.command()
@click.pass_context
def euler(ctx, **kwargs):
    args = dict(ctx.parent.args, **kwargs)

    step = args['step']
    x, y = (args['x0'], args['y0'])
    dydx = args['dydx']

    to_x = args['to_x']
    rows = []

    for x in frange(x, to_x, step):
        slope = eval(dydx)
        old_y = y
        y += slope * step

        rows.append([x, old_y, slope, x + step, y])

    rows.append([to_x, y])
    print(tabled(['Xn', 'Yn', 'k', 'Xn+1', 'Yn+1'], rows).table)


@cli.command()
@click.pass_context
def imeuler(ctx):
    args = ctx.parent.args
    step = args['step']
    x, y = (args['x0'], args['y0'])
    dydx = args['dydx']

    to_x = args['to_x']
    rows = []

    for x in frange(x, to_x, step):
        slope1 = eval(dydx)
        old_y = y
        u_y = y + slope1 * step
        slope2 = eval(dydx, globals(), {'x': x + step, 'y': u_y})
        
        y += step * (slope1 + slope2) / 2

        rows.append([x, old_y, slope1, u_y, slope2, x + step, y])

    rows.append([to_x, y])
    print(tabled(['Xn', 'Yn', 'k1', 'un+1', 'k2', 'Xn+1', 'Yn+1'], rows).table)


if __name__ == '__main__':
    cli()
