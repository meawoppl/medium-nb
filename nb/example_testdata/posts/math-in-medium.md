# Math Typesetting in Medium
$
 \rho \left( \frac{\partial \mathbf{u}}{\partial t} + \mathbf{u} \cdot \nabla \mathbf{u} \right) = - \nabla \bar{p} + \mu \nabla^2 \mathbf u + \tfrac13 \mu \nabla (\nabla\cdot\mathbf{u}) + \rho\mathbf{g}
$

I occasionally find the the Medium publishing platform frustrating.  It
supports only a hyper-minimal set of formatting possibilities, 
which preclude the ability to:

* Center/Justify/Align text
* Have more than one space at the end of a sentence
* Indent a paragraph
* Embed Javascript

I still use it because its weaknesses are also its largest strengths.
With minimalism comes a very clean UI and a very tight aesthetic. A minimal
formatting pallet isn't really a deal breaker for most writing.  We don't really
need for "House of Leaves" style formatting for the day-to-day. That
said, it limits the sorts of poetry one can compose and 
**it makes science writing pretty much impossible**.  

Today I became pretty annoyed with this this whole situatiuon, and I decided
to do something about it.  My original intention was to make something to syncronize
my local notebooks (markdown/html) in the medium platform, and allow fo editing
to flow forwards/backwards between the two platforms.  But...

**The Medium API is write-only.**

When I say write-only, I mean that you actually can't even use it to update an
article or see what articles you have written! **C'mon guys.**

That said at the end of this all, a did have a thing that let you
typeset and upload equations.  Every so often you really need to say something
like

$
 e^{\pi i} + 1 = 0
$
or explain that the way to calculate inductance is given by
$
 L_{m,n} = \frac{\mu_0}{4\pi} \oint_{C_m}\oint_{C_n} \frac{d\mathbf{x}_m\cdot d\mathbf{x}_n}{|\mathbf{x}_m - \mathbf{x}_n|}
$

I don't want to host my own website and get all the annoying CSS right for
every platform/browser, so I guess this is an upgrade.

The [code is freely available](https://github.com/meawoppl/medium-nb),
and comes with a command line tool which:

* Reads a markdown file with embedded LaTeX.  
* Generates `.png` file graphics
* Uploads the images to Medium
* Replaces the LaTeX in the markdown document with the image links
* Uploads it all as a draft to your medium account

Its incomplete, overly simple, and a bit hacky, but hey:
$
 \mathrm{I\,can\,center\,text\,now!}
$

Enjoy.