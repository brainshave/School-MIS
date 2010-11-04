(defproject mis.random "0.1.0-SNAPSHOT"
  :description "Program that display histogram of system pseudo-random
  number generator."
  :aot [#"mis\.random\..*"]
  :main mis.random.random
  :omit-source true
  :jvm-opts ["-Xmx1g"]
  :dependencies [[org.clojure/clojure "1.2.0"]
		 [org.clojure/clojure-contrib "1.2.0"]
		 [little-gui-helper "0.1.0-SNAPSHOT"]
		 [com.miglayout/miglayout "3.7.3.1" :classifier "swt"]]
  :dev-dependencies [[swank-clojure "1.2.1"]])