FROM python:3.10

#ENV UV_LINK_MODE=copy

WORKDIR /project
RUN apt-get update && apt-get install -y git-lfs && rm -rf /var/lib/apt/lists/*
COPY . versa
RUN cd versa && git submodule update --init --recursive && pip install -e .
WORKDIR /project/versa/tools
RUN chmod +x *.sh
#RUN #./easy_install.sh
RUN ./install_asvspoof.sh
RUN ./install_audiobox-aesthetics.sh
RUN ./install_emo2vec.sh
RUN ./install_fadtk.sh
#RUN #./install_fairseq.sh
RUN ./install_nomad.sh
RUN ./install_noresqa.sh
#RUN #./install_pyannote.sh
RUN ./install_pysepm.sh
RUN ./install_scoreq.sh
RUN ./install_srmr.sh
RUN ./install_ssl-singer-identity.sh
RUN --mount=type=cache,target=/root/.cache/utmosv2 ./install_utmosv2.sh
RUN ./install_warpq.sh
RUN ./install_wvmos.sh
RUN ./setup_nisqa.sh
RUN . ./activate_utmosv2.sh

#COPY ./tests/resources/test.wav /project/data/input/test.wav
#COPY ./tests/resources/config.yml /project/data/config/config.yml

RUN mkdir /project/data
WORKDIR /project/data
## Let's download all relevant model weights
#RUN versa-score --score_config /project/data/config/config.yml --pred /project/data/input --output_file /project/data/output/output.jsonl --io dir

