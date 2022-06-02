FROM rabbitmq:3-management

# RUN apt-get clean && \
#     apt-get update && \
#     apt-get upgrade --yes --fix-broken --fix-missing --verbose-versions && \
#     apt-get install --yes --fix-broken --fix-missing --verbose-versions --no-install-recommends \
#       dnsutils inetutils-ping iproute2

RUN mkdir -p /etc/rabbitmq/certs
RUN chown rabbitmq:rabbitmq /etc/rabbitmq/certs

COPY --chown=rabbitmq:rabbitmq --chmod=0400 ./certs/server_wildcard.local_certificate.pem /etc/rabbitmq/certs
COPY --chown=rabbitmq:rabbitmq --chmod=0400 ./certs/server_wildcard.local_key.pem /etc/rabbitmq/certs

COPY --chown=rabbitmq:rabbitmq --chmod=0400 erlang.cookie /var/lib/rabbitmq/.erlang.cookie
COPY --chown=rabbitmq:rabbitmq --chmod=0600 enabled_plugins /etc/rabbitmq/
COPY --chown=rabbitmq:rabbitmq --chmod=0400 rabbitmq-env.conf /etc/rabbitmq/
COPY --chown=rabbitmq:rabbitmq --chmod=0400 rabbitmq.conf /etc/rabbitmq/
COPY --chown=rabbitmq:rabbitmq --chmod=0400 advanced.config /etc/rabbitmq/
COPY --chown=rabbitmq:rabbitmq --chmod=0400 inet_dist_tls.config /etc/rabbitmq

EXPOSE 4369 5671 5672 15672 15692 25672 35672-35682
