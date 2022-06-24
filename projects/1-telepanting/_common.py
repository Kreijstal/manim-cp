from manim import *
from core import *

# prefix sum animation
def psumAnim(A):
    ps = [0]
    for x in A:
        ps += [ x + ps[-1] ]

    class Main(Scene):
        def construct(self):
            pass

class Portal(ABWComponent):
    rainbow = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
    DDR = DEFAULT_DOT_RADIUS*2
    i = 0
    def __init__(self, **kwargs):
        props = {
            "x": 1,
            "y": 0,
            "ax": None,
            "open": True,
            "color": Portal.rainbow[Portal.i],
        }
        my = self.props = Namespace(props, kwargs)
        r = Portal.DDR if my.open else 0.0001 * Portal.DDR
        mobs = {
            'entrance': Dot(radius=1.5*Portal.DDR, point=my.ax.n2p(my.x), color=my.color),
            'exit': Dot(radius=.75*Portal.DDR, point=my.ax.n2p(my.y), color=my.color),
            'opening': Dot(radius=r, point=my.ax.n2p(my.x), color=BLACK),
        }
        super().__init__(my, mobs, kwargs)
        Portal.i = (Portal.i + 1) % len(Portal.rainbow)

    def toggle(self):
        p = self.props
        m = self.mobs
        p.open = not p.open
        if p.open:
            return ScaleInPlace(m.opening, 10000)
        else:
            return ScaleInPlace(m.opening, 0.0001)

class Ant(ABWComponent):
    def __init__(self, **kwargs):
        props = {
            "pos": 0,
            "color": PURE_RED,
            "ax": None
        }
        my = self.props = Namespace(props, kwargs)
        DDR = DEFAULT_DOT_RADIUS
        mobs = {
            'dot': Dot(my.ax.n2p(my.pos), color=my.color, radius=DDR * 2.2),
            #'label': Tex('A', font_size=22, color=invert_color(my.color)).move_to(my.ax.n2p(my.pos)),
            'eye': Dot(my.ax.n2p(my.pos) + UP * .02 + RIGHT * .075,
                       color=BLACK, radius=DDR * .5)
        }
        super().__init__(my, mobs, kwargs)

    def anim_pos(self):
        ax = self.props.ax
        pos = self.props.pos
        return self.mob.animate.move_to(ax.n2p(pos))

    def move(self, scene, portals):
        a = self.props
        a.pos += 1
        for portal in portals:
            p = portal.props
            if a.pos - 1 == p.x and p.open:
                a.pos = portal.props.y
                scene.play(self.anim_pos(), portal.toggle())
                return self.move(scene, portals)
        return self.anim_pos()

class Timer(ABWComponent):
    def __init__(self, **kwargs):
        props = {
            't': 0
        }
        my = self.props = Namespace(props, kwargs)
        mobs = {
            'text': Tex(r't = '),
            'val': Integer(my.t),
        }
        super().__init__(my, mobs, kwargs)
        self.mob.arrange(RIGHT)
        self.mob.shift(UP)


    def tick(self):
        m = self.mobs
        self.props.t += 1
        return [ApplyWave(m.text, run_time=1),
                ApplyWave(m.val, run_time=1),
                m.val.animate.set_value(self.props.t)]


def createPortals(tuples, ax):
    res = []
    for x, y, o in tuples:
        res.append(Portal(x=x,y=y,open=o,ax=ax))
    return res

