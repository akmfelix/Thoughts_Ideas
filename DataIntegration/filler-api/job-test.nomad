variable "image" {
  type = string
}

variable "namespace" {
  type = string
}

variable "token" {
  type = string
}

variable "addr" {
  type = string
}

variable "auth_fpath" {
  type        = string
  default     = "local/clients.json"
}

job "filler-api-test" {
  region      = "test"
  datacenters = ["test"]
  namespace   = var.namespace
  type        = "service"

  constraint {
    attribute = "${attr.kernel.name}"
    value     = "linux"
  }

  update {
    stagger           = "30s"
    max_parallel      = 1
    min_healthy_time  = "30s"
    healthy_deadline  = "5m"
    progress_deadline = "15m"
    auto_revert       = true
    canary            = 0
  }

  group "services-test" {
    count = 1

    restart {
      attempts = 5
      interval = "2m"
      delay    = "15s"
      mode     = "delay"
    }

    network {
      port "filler-port" {}
    }

    service {
      name = "filler"
      port = "filler-port"

      tags = [
        "${NOMAD_ALLOC_INDEX}",
        "traefik.enable=true",
        "traefik.http.routers.filler.rule=Host(`filler.service.test.consul`)",
        "traefik.http.routers.filler.entrypoints=web",
        "traefik.http.routers.filler.middlewares=redirectsecure@file",
        "traefik.http.routers.filler-secure.middlewares=service-replacepathregex@file",
        "traefik.http.routers.filler-secure.rule=Host(`filler.service.test.consul`)",
        "traefik.http.routers.filler-secure.entrypoints=websecure"
      ]

      check {
        type     = "tcp"
        port     = "filler-port"
        interval = "10s"
        timeout  = "2s"
      }
  
    }

    task "filler-api-test" {
      driver = "docker"

      vault {
        policies = ["almaty-di-storage", "almaty-di-kafka", "almaty-di-agreements", "di"]
      }

      config {
        network_mode = "host"
        image        = var.image
        labels {
          log_collect   = "true"
          space         = "di"
          service       = "filler-api"
          log_structure = "default_api"
        }
      }

      env {
        DIRECTUS_URL                = "https://sc-dutygraphic-mgmt.directus.halykbank.nb/items/Contact?filter[Value][_contains]={phone}&fields[]=Value"
        API_MODE                    = "TEST"
        HTTP_PROXY                  = "http://fgtsrv.halykbank.nb:8080"
        HTTPS_PROXY                 = "http://fgtsrv.halykbank.nb:8080"
        NO_PROXY                    = "localhost,host.docker.internal,analytics-test-kafka.service.almaty.consul"
        SERVICE_PORT                = "${NOMAD_HOST_PORT_filler-port}"
        TOPIC                       = "offers-interest"
        DUAT_DATABASE_SCHEMA        = "duatdb"
        DEPLOY_ENV                  = "test"
        REFERENCE_UL_AUTH_ENABLED   = "true"
        CLOSED_ACCOUNT_AUTH_ENABLED = "true"
        AUTH_FPATH                  = "/${var.auth_fpath}"
      }

      template {
        destination = "local/file.env"
        env         = true
        data        = file("secrets.test.vault")
      }

      template {
        destination = "${var.auth_fpath}"
        data        = file("secrets/auth.test.vault")
      }

      resources {
        cpu    = 113
        memory = 512
      }
    }
  }
}
