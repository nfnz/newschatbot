variable "aws-region" {
  type    = string
  default = "eu-west-3"
}

variable "codename" {
  type    = string
  default = "newschatbot"
}

# Internal domain, its not visible publicly, but it should be domain we own
# to comply with best practices => it ensures the internal domain names are globally unique.
variable "codename-domain" {
  type    = string
  default = "newschatbot.ceskodigital.net"
}

variable "database-username" {
  type    = string
  default = "newschatbotdevelopment"
}

variable "database-password" {
  type = string
}
