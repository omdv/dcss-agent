# Progression
Level 1.0: Basic LLM with prompt

Single agent, tasked to explore and fight. Able to load the game and navigate around. Generally has no issues picking the right shortcut, however fails to do anything strategic, like skill setup.

```code
2025-04-08 21:12:47.625 | INFO     | __main__:<module>:21 - Welcome to Erheju Voash's Armour Shoppe! What would you like to do?
 a -   45 gold   a +0 buckler
 b -  670 gold   +1 fire dragon scales
 c -   20 gold   a +0 leather armour
 d -   20 gold   a +0 leather armour
 e -   20 gold   a +0 leather armour
 f -   20 gold   a +0 leather armour
 g -   45 gold   a +0 pair of gloves
 h -  230 gold   a +0 plate armour
 i -   40 gold   a +0 ring mail
 j -   40 gold   a +0 ring mail
 k +    7 gold   a +0 robe
 l -    7 gold   a +0 robe

You have 7 gold pieces. After the purchase, you will have 0 gold pieces.
[Esc] exit          [!] buy|examine items       [a-l] mark item for purchase
[/] sort (type)     [Enter] buy marked items    [A-L] put item on shopping list
2025-04-08 21:12:49.656 | DEBUG    | src.agents.basic:get_agent_action:30 - Result: {"key": "k", "reason": "Out of the available items, you only have 7 gold pieces, which allows you to purchase a +0 robe, option 'k'. This will leave you with no gold left, but it's affordable within your budget."}
```

It also has issues with complex navigation, like firing projectiles, which is critical for wizard classes, for instance it cannot get out of this loop.

```code
2025-04-08 21:14:11.173 | INFO     | __main__:<module>:21 - SomeSent key tab the Charlatan
               ###                   Spriggan
               #..                   Health: 9/9       ========================
          #### #.#                   Magic:  2/2       ========================
           ... #.#                   AC:  2            Str: 8
            #.##.######              EV: 16            Int: 12
       ######.........#              SH:  0            Dex: 15
       ....$........#.#              XL:  1 Next: 58%  Place: Dungeon:1
       .r#######@##.#.#              Noise: ---------  Time: 216.8 (0.0)
               #.##.#.#              a) +0 club
               #.##.#.#              Zap: wand of iceblast (1)
               #.#....####.
               #...........
               #.#...#####
               #.##.##
               #.##..#
               #.###.#
 Uppercase [Y]es or [N]o only, please.
 That beam is likely to hit you. Continue anyway?
_Okay, then.
_A rat is nearby!
_A rat is nearby!
_A rat is nearby!
2025-04-08 21:14:12.493 | DEBUG    | src.agents.basic:get_agent_action:30 - Result: {"key": "N", "reason": "To prevent self-damage from the iceblast, especially since health is relatively low and the rat might not be a significant threat."}
2025-04-08 21:14:12.493 | INFO     | __main__:<module>:23 - {'key': 'N', 'reason': 'To prevent self-damage from the iceblast, especially since health is relatively low and the rat might not be a significant threat.'}
```
