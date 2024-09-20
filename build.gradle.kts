plugins {
    id("application")
    id("com.gradleup.shadow") version "8.3.1"
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("ch.qos.logback:logback-core:1.5.7")
    implementation("ch.qos.logback:logback-classic:1.5.7")
    implementation("org.slf4j:slf4j-api:2.0.13")
    implementation("org.telegram:telegrambots-longpolling:7.10.0")
    implementation("org.telegram:telegrambots-client:7.10.0")
    implementation("org.telegram:telegrambots-meta:7.10.0")
}

java {
    toolchain {
	languageVersion = JavaLanguageVersion.of(17)
    }
}

tasks {
    shadowJar {
        minimize()
    }
}

application {
    mainClass = "me.t.realLiHua"
}
