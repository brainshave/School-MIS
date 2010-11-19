(ns mis.random.widgets
  (:require (mis.random [generator :as generator]
			[image :as image])
	    (little-gui-helper [properties :as props]))
  (:import (org.eclipse.swt.widgets Display Shell Button Composite Label Spinner
				    Canvas ProgressBar)
	   (org.eclipse.swt.events PaintListener ModifyListener SelectionListener)
	   (org.eclipse.swt.graphics Color)
	   (org.eclipse.swt SWT)
	   (net.miginfocom.swt MigLayout)))

(defn swt-async [f & args]
  (.asyncExec (Display/getDefault) #(apply f args)))

(defn control-panel [parent]
  (let [panel (Composite. parent SWT/NONE)
	layout (MigLayout.)
	n-label (props/doprops (Label. panel SWT/HORIZONTAL)
			       :text "Ilość losowań:")
	n-spinner (Spinner. panel SWT/NONE)
	max-lable (props/doprops (Label. panel SWT/HORIZONTAL)
				 :text "Maksymalna liczba:")
	max-spinner (Spinner. panel SWT/NONE)
	progress-bar (ProgressBar. panel (reduce bit-or [SWT/HORIZONTAL]))
	restart-button (Button. panel SWT/PUSH)]
    (props/doprops panel :layout layout)
    (dorun (map #(props/doprops %1
				:minimum 1
				:maximum Integer/MAX_VALUE
				:selection %2
				:layout-data "wrap")
		[n-spinner max-spinner]
		[30000 1000]))
    (props/doprops progress-bar
		   :minimum 0
		   :selection 0
		   :layout-data "span, wrap, grow")
    (add-watch generator/*progress* :watch-progress
	       (fn [_ _ _ progress] (swt-async #(.setSelection progress-bar progress))))
    (props/doprops restart-button
		   :text "Przelicz!"
		   :layout-data "span, center, wrap"
		   :+selection.widget-selected
		   (let [n (.getSelection n-spinner)
			 max (.getSelection max-spinner)]
		     (.setEnabled restart-button false)
		     (props/doprops progress-bar
				    :maximum (- n 2000)
				    :selection 0)
		     (swap! generator/*histogram-settings*
			    #(assoc %
			       :n n
			       :max max))))
    (add-watch generator/*histogram* :ungray-restart-button
	       (fn [& _] (swt-async #(.setEnabled restart-button true))))
    panel))

(defn general-canvas [parent]
  (let [canvas (Canvas. parent SWT/NO_BACKGROUND)]
    (props/doprops canvas
		   :+paint.paint-control
		   (image/draw-scaled-histogram
		    (.. event gc)
		    @generator/*histogram*
		    (:n @generator/*histogram-settings*)
		    (.getBounds canvas)))
    (add-watch generator/*histogram* :redraw-general-histogram
	       (fn [& _] (swt-async #(.redraw canvas))))))

(defn detail-canvas [parent]
  (let [canvas (Canvas. parent (reduce bit-or [SWT/NO_BACKGROUND
					       SWT/H_SCROLL]))]
    (props/doprops canvas
		   :+paint.paint-control
		   (image/draw-detail-histogram
		    (.. event gc)
		    @generator/*histogram*
		    (:n @generator/*histogram-settings*)
		    (.getBounds canvas)
		    0))
    
    (add-watch generator/*histogram* :redraw-detailhistogram
	       (fn [& _] (swt-async #(.redraw canvas))))
    canvas))
		   ;; (doto (.. event gc)
		   ;;   (.setBackground (Color. (Display/getDefault) 40 40 40))
		   ;;   (.fillRectangle 0 0
		   ;; 		     (.. canvas getBounds width)
		   ;; 		     (.. canvas getBounds height))))))

  
(defn open-shell
  "Creates new main window Shell, opens it and returns."
  [& args]
  (let [shell (Shell. (Display/getDefault))
	layout (MigLayout. "" "0[grow,fill][fill]0"
			   "0[300!,fill][grow,fill]0")
	general (general-canvas shell)
	control-panel (control-panel shell)
	detail (detail-canvas shell)]
    (props/doprops shell
		   :text (str "Badanie generatora liczb pseudo-losowych Javy"
			      " / Szymon Witamborski")
		   :size ^unroll (700 600)
		   :layout layout)
    (props/doprops detail :layout-data "span")
    ;;(props/doprops zoom-out-canvas :layout-data "grow")
    (props/doprops control-panel :layout-data "wrap")
    (.layout shell)
    (.open shell)
    shell))