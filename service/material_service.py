from urllib.parse import urlsplit, parse_qs, unquote


class MaterialService:

    @staticmethod
    def normalizar_url(url):
        if url is None or url.strip() == "":
            return None
        url = url.strip().strip('"\'').replace("\\", "/")
        partes = urlsplit(url)
        if partes.scheme.lower() in ("http", "https"):
            if not partes.hostname or partes.username or partes.password:
                raise ValueError("Informe um endereço válido para o material.")
            return url


        caminho = unquote(url)
        posicao = caminho.lower().find("/bucket/")
        if posicao >= 0:
            caminho = caminho[posicao + 1:]
        elif caminho.lower().startswith("bucket/"):
            caminho = "bucket/" + caminho[7:]
        else:
            raise ValueError("Informe um endereço http/https ou um arquivo dentro da pasta bucket.")
        if caminho[:7].lower() == "bucket/":
            caminho = "bucket/" + caminho[7:]
        segmentos = caminho.split("/")
        for segmento in segmentos:
            if segmento in (".", "..", "") or ":" in segmento or "\x00" in segmento:
                raise ValueError("O caminho do material é inválido.")
        return caminho

    @staticmethod
    def preparar(aula):
        try:
            url = MaterialService.normalizar_url(aula.url)
        except ValueError:
            return {"modo": "invalido", "url": None, "caminho": None, "embed": None}
        dados = {"modo": "nenhum", "url": url, "caminho": None, "embed": None}
        if not url:
            return dados
        tipo = aula.tipo.value
        if url.startswith("bucket/"):
            dados["caminho"] = url[7:]
            dados["modo"] = tipo if tipo in ("video", "audio", "imagem") else "arquivo"
            return dados

        partes = urlsplit(url)
        host = partes.hostname.lower()
        youtube = host in ("youtube.com", "www.youtube.com", "m.youtube.com",
                           "youtube-nocookie.com", "www.youtube-nocookie.com", "youtu.be", "www.youtu.be")
        if tipo == "video" and youtube:
            video_id = ""
            caminho = partes.path.strip("/").split("/")
            if host in ("youtu.be", "www.youtu.be"):
                video_id = caminho[0]
            elif partes.path == "/watch":
                video_id = parse_qs(partes.query).get("v", [""])[0]
            elif caminho[0] in ("embed", "shorts", "live") and len(caminho) >= 2:
                video_id = caminho[1]
            valido = len(video_id) == 11
            for letra in video_id:
                if letra not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-":
                    valido = False
            if valido:
                dados["modo"] = "youtube"
                dados["embed"] = "https://www.youtube.com/embed/" + video_id
                return dados
        extensao = partes.path.lower()
        if tipo == "video" and extensao.endswith((".mp4", ".webm", ".ogg", ".ogv", ".m4v")):
            dados["modo"] = "video"
        elif tipo == "audio":
            dados["modo"] = "audio"
        elif tipo == "imagem":
            dados["modo"] = "imagem"
        else:
            dados["modo"] = "link"
        return dados
