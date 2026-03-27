pipeline {
  agent any

  environment {
    GIT_DIFF_RANGE = "origin/master...HEAD"
    TOOL_VERSION = "v1.0-demo"
    LOCKFILE = "modules.json"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
        sh 'git fetch origin master --depth=1 || true'
      }
    }

    stage('Compute impact') {
      steps {
        script {
          def out = sh(script: 'python3 scripts/impacted_modules.py', returnStdout: true).trim()
          env.IMPACTED_MODULES = out
          echo "IMPACTED_MODULES=${env.IMPACTED_MODULES}"
        }
      }
    }

    stage('Cache key') {
      steps {
        script {
          def key = sh(script: 'python3 scripts/cache_key.py', returnStdout: true).trim()
          env.CACHE_KEY = key
          echo "CACHE_KEY=${env.CACHE_KEY}"
        }
      }
    }

    stage('Build & test') {
      steps {
        script {
          if (!env.IMPACTED_MODULES) {
            echo "No impacted modules, skipping build stage."
            return
          }
          env.IMPACTED_MODULES.split(',').each { mod ->
            echo "Building module: ${mod}"
            sh """
              mkdir -p build/${mod}
              echo "built-${mod}" > build/${mod}/artifact.txt
            """
          }
        }
      }
    }

    stage('Artifact metadata') {
      steps {
        sh 'python3 scripts/artifact_meta.py'
        stash includes: 'artifact_meta.json, build/**', name: "artifacts-${env.BUILD_ID}"
      }
    }

    stage('Upload artifacts (prototype)') {
      steps {
        echo "Prototype upload: would upload stashed artifacts here."
      }
    }
  }

  post {
    always {
      echo "CI metrics (prototype):"
      echo "  impacted=${env.IMPACTED_MODULES}"
      echo "  cache_key=${env.CACHE_KEY}"
    }
  }
}
