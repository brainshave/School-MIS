(ns mis.random.random
  (:gen-class)
  (:require (mis.random [widgets :as widgets]))
  (:import (org.eclipse.swt.widgets Display Shell)))

(defn swt-loop
  ([watched-shell]
     (loop [] (let [display (Display/getDefault)]
		(try
		  (if-not (.readAndDispatch display)
		    (.sleep display))
		  (catch Exception e (.printStackTrace e)))
		(if (and watched-shell (.isDisposed watched-shell))
		  (.dispose display)
		  (recur)))))
  ([] (swt-loop nil)))

(def *loop-thread* (atom nil))

(defn loop-background []
  (reset! *loop-thread* (doto (Thread. swt-loop)
			  (.start))))

(defn start-async [& args]
  (println "Async")
  (.asyncExec (Display/getDefault) #(apply widgets/open-shell args)))

(defn -main [& args]
  (println "Yellow World!")
  (swt-loop (apply widgets/open-shell args))
  (println "Bye World!"))
