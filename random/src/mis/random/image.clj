(ns mis.random.image
  (:import (org.eclipse.swt.graphics Color)
	   (org.eclipse.swt.widgets Display)))

(defn draw-scaled-histogram
  [gc histogram maximum bounds]
  (if (and gc histogram maximum bounds)
    (let [image-width (. bounds width)
	  image-height (. bounds height)
	  hist-size (count histogram)
	  step (/ hist-size image-width)
	  display (Display/getDefault)
	  white (Color. display 255 255 255)
	  black (Color. display 0 0 0)]
      (loop [i 0 x 0]
	(when (and (< i hist-size)
		   (< x image-width))
	  (let [border (int (- image-height (* (/ (aget histogram (int i))
						  maximum)
					       image-height)))]
	    (doto gc
	      (.setForeground white)
	      (.drawLine x 0 x (dec border))
	      (.setForeground black)
	      (.drawLine x image-height x border)))
	  (recur (+ i step) (inc x)))))))
  