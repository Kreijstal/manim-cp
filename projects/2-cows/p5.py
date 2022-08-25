from manim import *
from core import *
from common import *
from random import randint


class p5(Scene):
    def construct(self):

        cows = [(0, 0), (1, 1), (2, 2)]

        grid = make_grid(cows)
        self.play(FadeIn(grid.mob.shift(DOWN)))
        possible = Tex("Possible subsets", color=GREEN_E).shift(UP*2)
        impossible = Tex("Impossible subset", color=PURE_RED).move_to(possible)

        self.play(Create(possible))
        pg = gtr_enlarge(minimal_enclosures(grid, cows), grid, self, rt=1/3)

        a = [ScaleInPlace(grid[x][y].mobs.val, 1.4) for x, y in cows[::2]]
        a.extend(grid[x][y].anim_highlight(BLUE) for x, y in cows[::2])
        self.play(*a, run_time=1/3)
        self.wait(1)
        self.play(Transform(pg, grid.sub_grid(0, 0, 2, 2)), run_time=1/3)


        self.play(Transform(possible, impossible),
                  grid[1][1].anim_highlight(PURE_RED), run_time=1/3)

        # label = Tex("Number of subsets = ").shift(UP + LEFT)
        # self.add(label)
        # start = MathTex(0).next_to(label)

        # i = 1
        # cows = [(x // 10, x % 10) for x in range(20)]
        # grid = make_grid(cows, spot=DARK_BROWN, scale=1)
        # grid.mob.shift(DOWN)
        # for x, y in cows:
        #     i *= 2
        #     self.play(FadeIn(grid[x][y].mobs.val),
        #               Transform(start, MathTex(i).next_to(label)),
        #               run_time=.1)

        # s = "375828023454801203683362418972386504867736551759258677056523839782231681498337708535732725752658844333702457749526057760309227891351617765651907310968780236464694043316236562146724416478591131832593729111221580180531749232777515579969899075142213969117994877343802049421624954402214529390781647563339535024772584901607666862982567918622849636160208877365834950163790188523026247440507390382032188892386109905869706753143243921198482212075444022433366554786856559389689585638126582377224037721702239991441466026185752651502936472280911018500320375496336749951569521541850441747925844066295279671872605285792552660130702047998218334749356321677469529682551765858267502715894007887727250070780350262952377214028842297486263597879792176338220932619489509376"
        # ns = []
        # for i, x in enumerate(s):
        #     if i % 55 == 0:
        #         ns.append("\n")
        #     ns.append(x)
        # ns2 = []
        # for i, x in enumerate(str(randint(0, 9)) for x in range(80)):
        #     if i % 40 == 0:
        #         ns2.append("\n")
        #     ns2.append(x)

        # # fake precision
        # num_atoms = '8382925245689509501303493895917777710498\n\
        #     3268610770771142320951144532696957505379'

        # biggest_num = Tex(''.join(ns)).scale(.8)
        # equation = MathTex("2500^2 = 3.7 \\times 10^{753}")
        # atoms_mob = Tex(num_atoms)
        # self.play(Create(equation))
        # self.wait(1)
        # self.play(Transform(equation, biggest_num))
        # self.wait(1)
        # self.play(Transform(equation, atoms_mob))
        # self.wait(1)

        # Our first thought
        # may be to try each
        # subset and see if
        # it’s possible to enclose
        # only those cows. This
        # proves to be problematic.
        # Each additional cow doubles the number of possible subsets,
        # because we now
        # must consider every subset with that cow,
        # and every subset without that cow.
        # Even if we had an efficient
        # method to check whether a subset
        # is a valid enclosure [show invalid enclosures],
        # there are up to 2^2500 subsets of cows, which is considerably
        # more than the number of atoms in the universe.
