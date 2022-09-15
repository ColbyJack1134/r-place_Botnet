# r-place_Botnet
Code made during Reddit's r/place event, controls multiple Reddit accounts to place down images instead of just single pixels.

##Files:

placePixel.py  --  Main file, usage: python3 placepixle.py x y sten
     Places down the stencil at the x and y position provided
bean.sten  --  Example stencil of a bean guy
refreshBearers.py  --  Used to get the bearer tokens of your Reddit accounts
getSessionCookie.py  --  Used by refreshBearers.py to get the session cookie of an account
data/userlist.txt  --  Where you place the login details of your Reddit accounts
