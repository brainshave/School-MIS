(ns mis.random.image
  (:import (org.eclipse.swt.graphics Color)
	   (org.eclipse.swt.widgets Display)))

(let [display (Display/getDefault)
      white (Color. display 255 255 255)
      black (Color. display 0 0 0)]
  (defn draw-scaled-histogram
    [gc histogram maximum bounds]
    (if (and histogram maximum)
      (let [image-width (. bounds width)
	    image-height (. bounds height)
	    hist-size (count histogram)
	    step (/ hist-size image-width)]
	(loop [i 0 x 0]
	  (when (and (< i hist-size)
		     (< x image-width))
	    (let [border (int (- image-height (* (/ (aget histogram (int i))
						    maximum)
						 (/ hist-size 2)
						 image-height)))]
	      (doto gc
		(.setForeground white)
		(.drawLine x 0 x (dec border))
		(.setForeground black)
		(.drawLine x image-height x border)))
	    (recur (+ i step) (inc x)))))
      (.fillRectangle gc 0 0 (.width bounds) (.height bounds))))
  (defn draw-detail-histogram
    [gc histogram n bounds delta]
    (if (and histogram n)
      (let [image-width (. bounds width)
	    image-height (. bounds height)]
	    ;;y-delta (int (- (/ image-height 2) (/ n (count histogram))))]
	(dorun
	 (map-indexed 
	  #(let [border (- image-height %2)]
	     (comment %2)
	     (doto gc
	       (.setForeground white)
	       (.drawLine %1 0 %1 (dec border))
	       (.setForeground black)
	       (.drawLine %1 image-height %1 border)))
	  (drop delta (take image-width histogram))))
	(.fillRectangle gc (- (count histogram) delta) 0 (- image-width (- (count histogram) delta)) image-height))
      (.fillRectangle gc 0 0 (.width bounds) (.height bounds)))))
      