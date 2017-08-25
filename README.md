Jumpy Pig : A Game For Lila
===========================

My daughter loves pigs.
I love games.

Say hello to Jumpy Pig:

```      __,---.__        Oink!
      ,-'         `-.__  /
    &/           `._\ _\
    /               ''._
    |   ,             (")
    |__,'`-..--|__|--''
```


_"Jean Claude the donkey has gotten lost and only Jumpy Pig can rescue him!
Can you help Jumpy Pig save her friend?"_


# Ideas to add
--------------
- [ ] Collect mushrooms to: increase jump size? snort louder?
- [ ] Bouncy frogs (hit from above to get a big jump)
- [ ] Wake up sleeping animals to get past them
- [ ] Snort to wake up the donkey
- [ ] In game timer
- [ ] Obsticles that reset the level if you hit them (Jumpy runs back?)
- [ ] Jump control by holding the button


# Key Gameplay Concepts
-----------------------
Jumpy pig jumps. On things. Different things happen depending on what she
jumps on: bounce, alter the level, get a power up etc.


# Performance improvements
-------------------------
* Try having the Level rendered once and then used as a background. (Blit player
  onto the screen independently?)
* See if there is a way to combine sprite hitboxes...is this what the sprite
  group is doing already?
