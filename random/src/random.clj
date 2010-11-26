(ns random
  (:gen-class)
  (:use (little-gui-helper properties)
	(incanter core stats charts))
  (:import (javax.swing JFrame JPanel JLabel JButton
			JSpinner SpinnerNumberModel
			WindowConstants)
	   (java.awt.event ActionListener)
	   (net.miginfocom.swing MigLayout)))


(defn set-laf
  "Pomocnicza funkcja ustawiająca skórkę Swinga o nazwie laf."
  [laf]
  (try (->> (javax.swing.UIManager/getInstalledLookAndFeels)
	    (filter #(-> % .getName (= laf)))
	    first
	    .getClassName
	    javax.swing.UIManager/setLookAndFeel)
       (catch NullPointerException e)))

(defn lafs
  "Funkcja pomocnicza zwracająca nazwy dostępnych skórek Swinga."
  []
  (map #(.getName %)
       (javax.swing.UIManager/getInstalledLookAndFeels)))

(defn -open-frame []
  (let [frame (JFrame.)
	layout (MigLayout. "wrap 2" "[][fill,grow]" "[][][fill,grow]")
	tests-label (JLabel. "Ilość testów") 
	scope-label (JLabel. "Maksymalna liczba")
	tests-spinner (JSpinner. (SpinnerNumberModel. 10001 1 Integer/MAX_VALUE 5000))
	scope-spinner (JSpinner. (SpinnerNumberModel. 1001 1 Integer/MAX_VALUE 100))
	start-button (JButton. "Pokaż wykres")]
    (doprops frame
	     :title "Badanie właściwości liczb losowych / Szymon Witamborski"
	     :layout layout
	     :size ^unroll (500 200))
    (doprops start-button +action.action-performed
	     (let [tests (.getValue tests-spinner)
		   scope (.getValue scope-spinner)]
	       (view (histogram (repeatedly tests #(rand-int (inc scope)))
				:nbins scope
				:title (format "Wykres %d liczb od 0 do %d"
					       tests scope)
				:y-label "Ilość wystąpień"
				:x-label "Wartość"))))
    (doseq [x [tests-label tests-spinner
	       scope-label scope-spinner
	       start-button]]
      (.add frame x))
    (doprops layout 
	     :component-constraints ^unroll (start-button "span, grow"))
    (doprops frame :visible true)
    frame))
	   

(defn -main [& args]
  (set-laf "Nimbus")
  (doprops (-open-frame)
	   :default-close-operation WindowConstants/EXIT_ON_CLOSE))
	