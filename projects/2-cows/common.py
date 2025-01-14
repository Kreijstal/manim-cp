from manim import *
from core import *
from random import choice


class Cow(ABWComponent):
    def __init__(self, **kwargs):
        props = {
            "radius": .3,
            "spot": BLACK
        }
        my = self.props = Namespace(props, kwargs)
        r = my.radius

        skin = Circle(fill_opacity=1, stroke_width=0,
                      color=WHITE, radius=1*r)
        snout = Ellipse(fill_opacity=1, color='#FFA1E0',
                        stroke_width=0, width=1.1*r, height=.6*r)
        snout.shift(.7*DOWN*r)

        eyes = []
        nostrils = []
        spot_circles = []
        for x in [LEFT, RIGHT]:
            eyes.append(Circle(fill_opacity=1, stroke_width=0,
                               color=BLACK, radius=.15*r))
            eyes[-1].shift(UP*0*r)
            eyes[-1].shift(x*.3*r)

            nostrils.append(Ellipse(fill_opacity=1, stroke_width=0,
                                    width=.12*r, height=.08*r, color=BLACK))
            nostrils[-1].move_to(snout)
            nostrils[-1].shift(.1 * r * x)
            nostrils[-1].shift(DOWN*.08*r)

            spot_circles.append(Circle(radius=.5*r))
            spot_circles[-1].shift(x*r*.7)

        spot_circles.pop()
        spot_circles[-1].shift(UP*r*.6)

        spots = []
        for x in spot_circles:
            spots.append(Intersection(skin, x, color=my.spot,
                         fill_opacity=1, stroke_width=1))

        ordered_parts = [skin, *spots, *eyes, snout, *nostrils]
        whole_cow = VGroup(*ordered_parts)

        mobs = {
            "cow": whole_cow
        }
        super().__init__(my, mobs, kwargs)


class HashSet(ABWComponent):
    def __init__(self, **kwargs):
        props = {
            "height": 3,
            "width": 3,
            "color": BLACK,
            "outline": WHITE,
            "count": 0,
            "set": set([-1]),
        }
        my = self.props = Namespace(props, kwargs)
        my.fs = fs = 10*my.width
        mobs = {
            "box": Rectangle(color=my.outline, fill_opacity=1, fill_color=my.color,
                             height=my.height, width=my.width),
            "label": Tex("HashSet", font_size=fs),
            "counter": Integer(my.count, font_size=fs),
            "text": Tex("Distinct subsets: ", font_size=fs),
            "error": Tex("Already counted", font_size=fs, color=RED),
            "success": Tex("New subset", font_size=fs, color=GREEN),
        }
        super().__init__(my, mobs, kwargs)
        my.buffer = my.width*.04
        m = self.mobs
        m.label.shift(UP*.3*my.height)
        m.counter.move_to(m.text).next_to(m.text, RIGHT, buff=my.buffer)
        VGroup(m.text, m.counter).move_to(m.box).shift(UP*.1*my.height)
        m.error.shift(DOWN*.35*my.height).scale(1/10000)
        m.success.move_to(m.error).scale(1/10000)

    def put(self, mob, scene, val=None, rt=1):
        my = self.props
        m = self.mobs

        scale_factor = min(1, (3/4 * my.width) / width(mob))
        mob.generate_target()
        mob.target.move_to(m.box).shift(DOWN*.15*my.height)
        scene.play(ScaleAndMove(mob, scale_factor), run_time=rt)

        if val not in my.set or val is None:
            my.set.add(val)
            my.count += 1
            a = Integer(my.count, font_size=my.fs)
            a.move_to(m.counter)
            a.next_to(m.text, RIGHT, buff=my.buffer)

            scene.play(FadeOut(m.success, run_time=1/60))
            m.success.scale(10000)
            scene.play(Create(m.success), run_time=rt/4)
            scene.wait(rt/4)

            r = [FadeOut(m.counter), FadeIn(
                a), FadeOut(mob), FadeOut(m.success)]
            scene.play(*r, run_time=rt/2)
            self.mob.remove(m.counter)
            m.counter = a
            self.mob.add(m.counter)
            m.success.scale(1/10000)

        else:
            scene.play(FadeOut(m.error, run_time=1/60))
            m.error.scale(10000)
            scene.play(Create(m.error), run_time=rt/4)
            scene.wait(rt/2)
            scene.play(FadeOut(mob), FadeOut(m.error), run_time=rt/2)
            m.error.scale(1/10000)


class CoordinateList(ABWComponent):
    def __init__(self, **kwargs):
        props = {
            "coords": [],
            "coords_mobs": [],
            "scale": 1
        }
        my = self.props = Namespace(props, kwargs)
        mobs = {
            "starter": Circle(stroke_width=0, fill_opacity=0, radius=0),
            "cursor": Circle(stroke_width=0, fill_opacity=0, radius=0)
        }
        super().__init__(my, mobs, kwargs)

    def append(self, mob, pair):
        my = self.props
        my.coords.append(pair)
        my.coords_mobs.append(mob)
        self.mob.add(mob)

    def AddWithFade(self, x, y):
        my = self.props
        mobs = []
        for s in f"({x},{y})":
            mobs.append(MathTex(s))
            mobs[-1].next_to(self.mob, RIGHT, buff=.1*my.scale).scale(my.scale)
            self.mob.add(mobs[-1])
        self.mob.remove(*mobs)
        mobs[2].shift(DOWN*.2*my.scale)
        new_mob = VGroup(*mobs)
        self.append(new_mob, (x, y))
        return FadeIn(new_mob)

    def AddFromAxes(self, x, y, grid, rate_func=smooth):
        my = self.props
        pre = ',' if my.coords else ''
        s1 = f"{pre}({x},{y})"
        mobs = []
        for i, s in enumerate(s1):
            mobs.append(MathTex(s))
            if i == 0:
                mobs[-1].next_to(self.mobs.cursor, RIGHT, buff=-.1)
            else:
                buff = .2*my.scale if (len(s1) == 6 and i ==
                                       1) else .1*my.scale
                mobs[-1].next_to(mobs[-2], RIGHT, buff=buff)
            self.mob.add(mobs[-1])

        self.mob.remove(*mobs)
        self.mobs.cursor.next_to(mobs[-1], RIGHT)

        mobs[-3].shift(DOWN*.2*my.scale)
        if len(mobs) == 6:
            mobs[0].shift(DOWN*.2*my.scale)

        x1, y1 = grid.mobs.x_axis[y], grid.mobs.y_axis[x]
        x2, y2 = x1.copy(), y1.copy()
        res = [Transform(x2, mobs[-2], rate_func=rate_func),
               Transform(y2, mobs[-4], rate_func=rate_func)]

        mobs.pop(-4)
        mobs.pop(-2)

        res += [FadeIn(x, rate_func=rate_func) for x in mobs]
        new_mob = VGroup(*mobs, x2, y2)
        self.append(new_mob, (x, y))
        return res

    def reset(self):
        my = self.props
        my.coords = []
        res = [FadeOut(x) for x in my.coords_mobs]
        for x in my.coords_mobs:
            self.mob.remove(x)
        my.coords_mobs = []
        self.mobs.cursor.move_to(self.mobs.starter)
        return res

    def pop(self, scene):
        nl = self.mob.copy()
        scene.add(nl)
        scene.remove(*self.props.coords_mobs)
        res = tuple(self.props.coords)
        if res:
            scene.play(*self.reset(), run_time=1/60)
        return nl, res


def make_grid(points, spot=BLACK, **kwargs):
    n = max(points)[0] + 1
    m = max(points, key=lambda x: x[1])[1] + 1
    mtx = [[None for _ in range(m)] for _ in range(n)]
    for x, y in points:
        mtx[x][y] = Cow(spot=spot).mob
    return Grid(mtx, **kwargs)


def unwrap_rects(grid):
    res = []
    for x1 in range(grid.props.nx):
        for y1 in range(grid.props.ny):
            for x2 in range(x1, grid.props.nx):
                for y2 in range(y1, grid.props.ny):
                    res.append((x1, y1, x2, y2))
    return res


def go_through_rects(rects_list, grid, scene, rt=1/6, pg=None, **kwargs):
    for rect in rects_list:
        ng = grid.sub_grid(*rect, **kwargs)
        if pg is None:
            pg = ng
            scene.play(FadeIn(pg), run_time=rt)
        else:
            scene.play(Transform(pg, ng), run_time=rt)
        scene.wait(rt)
    return pg


def squish_helper(anim_queue):
    def end_time(x): return x[1] + x[2]
    total = end_time(max(anim_queue, key=end_time))
    res = []
    for func, start_time, run_time, args, kwargs in anim_queue:
        a = start_time/total
        b = (start_time + run_time) / total
        rf = squish_rate_func(smooth, a, b)
        try:
            res.extend(func(*args, **kwargs, rate_func=rf))
        except TypeError:
            res.append(func(*args, **kwargs, rate_func=rf))
    return res, total


def sweep(rect, grid, cl, rt=1 / 12):
    t = 0
    anim_queue = []
    r = grid.cells_in_rect(*rect)
    for x, y, c in r:
        if is_cow(c):
            anim_queue.append((c.anim_highlight, t, rt, [GREEN], {}))
            anim_queue.append((cl.AddFromAxes, t, rt*4, [x, y, grid], {}))
        else:
            anim_queue.append((c.anim_highlight, t, rt, [RED], {}))
        t += rt
    return squish_helper(anim_queue)


def right(rect):
    cpy = list(rect)
    cpy[1] = cpy[3]
    return tuple(cpy)


def n6_alg(grid, scene, cl, hs, rt=1/6):
    pg = grid.sub_grid(0, 0, 0, 0)
    scene.play(FadeIn(pg), run_time=rt)

    for rect in unwrap_rects(grid)[:40]:
        # new enclosure
        ng = grid.sub_grid(*rect)
        scene.play(Transform(pg, ng), run_time=rt)
        scene.wait(rt)

        # sweep
        anims, run_time = sweep(rect, grid, cl, rt=rt/2)
        scene.play(*anims, run_time=run_time)

        scene.wait(rt/2)
        # hashset insertion
        nl, res = cl.pop(scene)
        if res:
            hs.put(nl, scene, val=res, rt=rt*3)
        scene.remove(nl)

        # reset
        scene.play(*grid.remove_highlights())


def n5_alg(grid, scene, cl, hs, rt=1/6):
    pg = grid.sub_grid(0, 0, 0, 0)
    scene.play(FadeIn(pg), run_time=rt)
    w = 0

    for rect in unwrap_rects(grid)[:25]:
        # new enclosure
        ng = grid.sub_grid(*rect)
        nw = width(ng)
        # reset when shrinking
        if nw <= w:
            scene.play(*grid.remove_highlights(), *cl.reset())
        w = nw
        scene.play(Transform(pg, ng), run_time=rt)
        scene.wait(rt)

        # sweep
        pc = len(cl.props.coords)
        anims, run_time = sweep(right(rect), grid, cl, rt=rt/2)
        scene.play(*anims, run_time=run_time)
        nc = len(cl.props.coords)
        scene.wait(rt/2)

        # hashset insertion
        if nc > pc:
            nl = cl.mob.copy()
            hs.put(nl, scene, val=tuple(cl.props.coords), rt=rt*3)

    scene.play(*grid.remove_highlights())


def maps(cows):
    x_map, y_map = {}, {}
    for x, y in cows:
        x_map[x] = y
        y_map[y] = x
    return x_map, y_map


def is_minimal(rects, x_map, y_map):
    x1, y1, x2, y2 = rects
    res = []
    for x in [x1, x2]:
        res.append(x in x_map and y1 <= x_map[x] <= y2)
    for y in [y1, y2]:
        res.append(y in y_map and x1 <= y_map[y] <= x2)
    return all(res)

# returns corner coordinates for all minimal enclosures


def minimal_enclosures(grid, cows):
    x_map, y_map = maps(cows)
    a = unwrap_rects(grid)
    return [c for c in a if is_minimal(c, x_map, y_map)]

# pass result into make_grid


def gen_random_pasture(num_cows, mx, my):
    x_set = list(range(mx))
    y_set = list(range(my))
    res = []
    for _ in range(num_cows):
        e = (choice(x_set), choice(y_set))
        res.append(e)
        x_set.remove(e[0])
        y_set.remove(e[1])
    return res


def is_cow(cell):
    try:
        cell.mobs.val
        return True
    except AttributeError:
        return False


def compress_grid(cows):
    x_map, y_map = maps(cows)
    sx = {x: i for i, x in enumerate(sorted(y_map.values()))}
    sy = {x: i for i, x in enumerate(sorted(x_map.values()))}
    new_cows = []
    for x, y in cows:
        new_cows.append((sx[x], sy[y]))
    return new_cows


def get_cow_cells(rect, grid):
    cows = []
    r = grid.cells_in_rect(*rect)
    for x, y, c in r:
        if is_cow(c):
            cows.append(c)
    return cows


def gtr_enlarge(rects_list, grid, scene, rt=1/6, pg=None, **kwargs):
    for rect in rects_list[i:]:
        ng = grid.sub_grid(*rect, **kwargs)
        cows = get_cow_cells(rect, grid)
        a = [ScaleInPlace(x.mobs.val, 1.4) for x in cows]
        a += [x.anim_highlight(BLUE) for x in cows]
        scene.play(*a, run_time=rt/2)
        scene.wait(rt)
        if pg is None:
            pg = ng
            scene.play(FadeIn(pg), run_time=rt/2)
        else:
            scene.play(Transform(pg, ng), run_time=rt/2)
        scene.wait(rt)
        a = [ScaleInPlace(x.mobs.val, 1/1.4) for x in cows]
        a.extend(grid.remove_highlights())
        scene.play(*a, run_time=rt/2)
        scene.wait(rt)
    return pg
