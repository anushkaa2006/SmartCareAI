# =====================================================
# SmartCare ID - Backend Dockerfile (multi-stage build)
# =====================================================

# ---- Stage 1: Build ----
# pom.xml pins java.version=25, so the build image must ship a JDK 25 toolchain.
# If your Docker/Maven registry does not yet have this tag available, either
# swap it for a JDK 25 image you do have access to, or lower <java.version>
# in backend/pom.xml to a JDK you have (e.g. 21) and use eclipse-temurin:21 below.
FROM maven:3.9-eclipse-temurin-25 AS build

WORKDIR /app

# Copy only the pom first to leverage Docker layer caching for dependencies
COPY pom.xml .
COPY .mvn .mvn
COPY mvnw .
RUN mvn -q -B dependency:go-offline || true

# Now copy the rest of the source and build
COPY src ./src
RUN mvn -q -B clean package -DskipTests

# ---- Stage 2: Run ----
FROM eclipse-temurin:25-jre-jammy

WORKDIR /app

# Create a non-root user to run the app
RUN useradd -ms /bin/bash spring
USER spring

# Copy the built artifact (jar or war, spring-boot-maven-plugin repackages both as runnable)
COPY --from=build /app/target/*.war app.war

EXPOSE 9090

ENTRYPOINT ["java", "-jar", "/app/app.war"]
