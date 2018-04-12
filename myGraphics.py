# Smith, Mitchel J.R.
# 1000-799-110
# 2018-02-27

#----------------------------------------------------------------------
# This code was originally created by Prof. Farhad Kamangar.
# It has been somewhat modified and updated by Brian A. Dalio for use
# in CSE 4303 / CSE 5365 in the 2018 Spring semester.

#----------------------------------------------------------------------
# https://en.wikipedia.org/wiki/Cohen-Sutherland_algorithm

INSIDE = 0
LEFT   = 1
RIGHT  = 2
BELOW  = 4
ABOVE  = 8

#------------------------------------------------------------
# clipLine( p1x, p1y, p2x, p2y, portal )
#   p1x, p1y -- the coordinates of point 1.
#   p2x, p2y -- the coordinates of point 2.
#   portal   -- a list of the viewport region limits
#               in this order:
#                 [ xmin, ymin, xmax, ymax ]
#
# returns ( doDraw, p1x, p1y, p2x, p2y )
#   doDraw   -- True if the line should be drawn, False if not.
#   p1x, p1y -- the new coordinates of point 1.
#   p2x, p2y -- the new coordinates of point 2.
#
def clipLine( p1x, p1y, p2x, p2y, portal ) :
  ( xMin, yMin, xMax, yMax ) = portal

  # In which region is each of the endpoints?
  p1Code = _regionCode( p1x, p1y, xMin, yMin, xMax, yMax )
  p2Code = _regionCode( p2x, p2y, xMin, yMin, xMax, yMax )

  # Loop until we have a definite accept or reject.
  while ( True ) :
    if ( ( p1Code | p2Code ) == 0 ) :
      # Both points have code 0000 and are therefore inside
      # the clipping region.  Trivial accept.
      doDraw = True
      break

    if ( ( p1Code & p2Code ) != 0 ) :
      # Both points outside on same side, either above, below,
      # left, or right of the region.  Trivial reject.
      doDraw = False
      break

    # Neither both out in a convenient way nor both in.  We have
    # to clip the line so that it's 'closer' to being out of the
    # region conveniently or entirely in the region.

    # Get the code of a point that is outside.  Both points
    # cannot be INSIDE (as we would have accepted above), so
    # if p1 in INSIDE, we use p2, otherwise p1.
    aRegionCode = p2Code if p1Code == INSIDE else p1Code

    # For that point, compute another point that is on the same
    # line, but at the corresponding edge of the region.

    if ( aRegionCode & ABOVE ) :
      # Point was ABOVE.  Move it along the line down to Y max.
      x = p1x + ( p2x - p1x )*( yMax - p1y )/( p2y - p1y )
      y = yMax

    elif ( aRegionCode & BELOW ) :
      # Point was BELOW.  Move it along the line up to Y min.
      x = p1x + ( p2x - p1x )*( yMin - p1y )/( p2y - p1y )
      y = yMin

    elif ( aRegionCode & RIGHT ) :
      # Point was to the RIGHT.  Move it along the line over to X max.
      x = xMax
      y = p1y + ( p2y - p1y )*( xMax - p1x )/( p2x - p1x )

    elif ( aRegionCode & LEFT ) :
      # Point was to the LEFT.  Move it along the line over to X min.
      x = xMin
      y = p1y + ( p2y - p1y )*( xMin - p1x )/( p2x - p1x )

    else :
      # Huh?  We didn't match _any_ region?  How did that happen?
      raise ValueError( 'code %s did not match any region?' % aRegionCode )

    # Replace whatever point we chose with the newly computed point.
    # We also have to recompute its region code.
    if ( aRegionCode == p1Code ) :
      # We were looking at p1.  Update its location and its code.
      p1x = x
      p1y = y
      p1Code = _regionCode( p1x, p1y, xMin, yMin, xMax, yMax )

    else :
      # We were looking at p2.  Update its location and its code.
      p2x = x
      p2y = y
      p2Code = _regionCode( p2x, p2y, xMin, yMin, xMax, yMax )

    # and now we do the loop again.

  # At this point, we have exited the loop and doDraw is True if
  # there's something to draw;  that is, if (eventually) there are
  # two points inside the draw region.
  # Either or both of p1 and p2 may have had their elements changed
  # so we have to return both to the caller.

  return ( doDraw, p1x, p1y, p2x, p2y )

#----------------------------------------------------------------------
# Computes the region code for the point x, y against the
# clipping region bounded by xMin, yMin, xMax, yMax.
def _regionCode( x, y, xMin, yMin, xMax, yMax ) :
  code = INSIDE

  # We use different bits for each 'side': LEFT, RIGHT, BELOW,
  # and ABOVE.  That way we can bitwise OR each bit in and still
  # keep them distinct.

  if ( x < xMin ) :
    code = code | LEFT
  elif ( x > xMax ) :
    code = code | RIGHT

  if ( y < yMin ) :
    code = code | BELOW
  elif ( y > yMax ) :
    code = code | ABOVE

  return code

#----------------------------------------------------------------------
class cl_world :
    def __init__( self, objects = [], canvases = [] ) :
        self.objects = objects
        self.canvases = canvases

    def add_canvas( self, canvas ) :
        self.canvases.append( canvas )
        canvas.world = self

    def create_graphic_objects( self, canvas, lines ) :

        for line in lines:
            if line[0] == 's':
                type,vx_min,vy_min,vx_max,vy_max = line.split()
            if line[0] == 'w':
                type,wx_min,wy_min,wx_max,wy_max = line.split()

        width = float(canvas.cget( "width" ))
        height = float(canvas.cget( "height" ))

        vx_min = float(vx_min)
        vy_min = float(vy_min)
        vx_max = float(vx_max)
        vy_max = float(vy_max)
        wx_min = float(wx_min)
        wy_min = float(wy_min)
        wx_max = float(wx_max)
        wy_max = float(wy_max)

        vx_min = vx_min * width
        vy_min = vy_min * height
        vx_max = vx_max * width
        vy_max = vy_max * height

        portal = [vx_min, vy_min, vx_max, vy_max]

        fx = wx_min * -1
        fy = wy_min * -1
        sx = ((vx_max - vx_min) / (wx_max - wx_min))
        sy = ((vy_max - vy_min) / (wy_max - wy_min))
        x = ((fx * sx) + vx_min)
        y = ((fy * sy) + vy_min)

        canvas.create_line(vx_min, vy_min, vx_min, vy_max, vx_max, vy_max, vx_max, vy_min, vx_min, vy_min)

        for line in lines:
            if line[0] == 'f':
                type, va, vb, vc = line.split()
                v1 = float(va) - 1
                v2 = float(vb) - 1
                v3 = float(vc) - 1

                vertices = []
                i = 0
                for l in lines:
                    if i == v1:
                        vertices.append(l)
                    i += 1

                i = 0
                for l in lines:
                    if i == v2:
                        vertices.append(l)
                    i += 1

                i = 0
                for l in lines:
                    if i == v3:
                        vertices.append(l)
                    i += 1

                x1 = 0
                x2 = 0
                x3 = 0
                y1 = 0
                y2 = 0
                y3 = 0

                j = 1
                for v in vertices:
                    type, m, n, z = v.split()
                    if j == 1:
                        x1 = m
                        y1 = n
                    if j == 2:
                        x2 = m
                        y2 = n
                    if j == 3:
                        x3 = m
                        y3 = n
                    j += 1

                x1 = float(x1)
                y1 = float(y1)
                x2 = float(x2)
                y2 = float(y2)
                x3 = float(x3)
                y3 = float(y3)

                xa = sx * x1 + x
                ya = sy * y1 + y
                xb = sx * x2 + x
                yb = sy * y2 + y
                xc = sx * x3 + x
                yc = sy * y3 + y

                doDraw, p1x, p1y, p2x, p2y = clipLine(xa, ya, xb, yb, portal)
                if doDraw:
                    canvas.create_line(p1x, p1y, p2x, p2y)

                doDraw, p1x, p1y, p2x, p2y = clipLine(xb, yb, xc, yc, portal)
                if doDraw:
                    canvas.create_line(p1x, p1y, p2x, p2y)

                doDraw, p1x, p1y, p2x, p2y = clipLine(xc, yc, xa, ya, portal)
                if doDraw:
                    canvas.create_line(p1x, p1y, p2x, p2y)

    def redisplay( self, canvas, event ) :
        if self.objects :
            canvas.coords(self.objects[ 0 ], 0, 0, event.width, event.height )
            canvas.coords(self.objects[ 1 ], event.width, 0, 0, event.height )
            canvas.coords(self.objects[ 2 ],
                int( 0.25 * int( event.width ) ),
                int( 0.25 * int( event.height ) ),
                int( 0.75 * int( event.width ) ),
                int( 0.75 * int( event.height ) ) )

#----------------------------------------------------------------------
