
to build tparty on ubuntu you need  the following non standart packages:


    https://github.com/DerThorsten/liquidfun  (build it with python wrapper and set the python path to my_liquidfun_builddir/python)


If you want to make an android build you need my python for android

    https://github.com/DerThorsten/python-for-android

and you need to  change the path in the buildozer.spec in tparty/buildozer.spec 
to your directory of my python for android fork (line 103)

# (str) python-for-android git clone directory (if empty, it will be automatically cloned from github)
android.p4a_dir = /home/tbeier/src/python-for-android