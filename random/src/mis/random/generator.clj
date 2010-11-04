(ns mis.random.generator)

(def *histogram-settings* (atom {:n 1 :max 1}))

(def *histogram* (agent nil))

(def *progress* (atom 0))

(defn histogram [n max]
  (let [hist (int-array max) n (int n)]
    (loop [num (rand-int max) i (int 0)]
      (if (< i n)
	(let [c (aget hist num)]
	  (if (zero? (rem i 1000)) (reset! *progress*  i))
	  (aset-int hist num (inc c))
	  (recur (rand-int max) (inc i)))
	(do (reset! *progress* 0)
	    hist)))))

(add-watch *histogram-settings* :recalc-histogram
	   (fn [_ _ _ {:keys [n max]}]
	     (send *histogram* (fn [_] (histogram n max)))))