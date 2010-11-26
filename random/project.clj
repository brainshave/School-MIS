(defproject random "1.0.0-SNAPSHOT"
  :description "Random number generator analyze"
  :main random
  ;;:aot ["random]
  :dependencies [[org.clojure/clojure "1.2.0"]
                 [org.clojure/clojure-contrib "1.2.0"]
		 [little-gui-helper "0.1.0-SNAPSHOT"]
		 [com.miglayout/miglayout "3.7.3.1" :classifier "swing"]
		 [incanter "1.2.3-SNAPSHOT"]]
  :dev-dependencies [[swank-clojure "1.2.1"]])

