# Baixando e Configurando a VM do PnetLab

## Download da VM

Faça o download da VM do PnetLab no link abaixo:

[Baixar VM do PnetLab](https://drive.google.com/drive/folders/1h8y6L2dacmzpYOo9l2sSziUeawlDEpuZ?usp=sharing)

Após concluir o download, extraia o arquivo `.zip` pelo terminal utilizando o comando `unzip`.

> [!NOTE]
> Adapte o caminho abaixo para o diretório onde o arquivo foi baixado.

```bash
cd Downloads
unzip vm-pnet.zip
```

---

# Importando o Appliance

![passo1](./screenshots/acessar-virtualbox.png)

Abra o VirtualBox e clique em **Importar**.

![passo2](./screenshots/escolhendo-ovf.png)

Selecione o arquivo `.ova` extraído anteriormente e clique em **Próximo**.

![passo3](./screenshots/importando-apliance.png)

Aguarde a importação do appliance ser concluída.

---

# Ajustes Necessários Após a Importação

Depois que a VM for importada, será necessário realizar alguns ajustes de rede.

![passo4](./screenshots/apertar-configuracoes.png)

Abra as configurações da VM e acesse:

```text
Configurações > Rede
```

Para cada adaptador de rede (Adaptador 1 e Adaptador 2), gere um novo endereço MAC clicando em:

```text
Avançado > Gerar novo endereço MAC
```

Após gerar novos endereços MAC para os dois adaptadores, clique em **OK**.

![passo5](./screenshots/gerar-novo-mac.png)

---

# Primeiro Boot da VM

Inicie a VM do PnetLab.

Faça login utilizando as seguintes credenciais:

```text
Usuário: root
Senha: pnet
```

Durante a inicialização, pressione `Enter` para confirmar as etapas de configuração padrão. Não é necessário alterar nenhuma opção.

Após a confirmação das etapas, a VM será reiniciada automaticamente.

Quando o sistema iniciar novamente, o PnetLab já poderá ser acessado:

- Via SSH
- Pelo navegador web

---

# Acessando a Interface Web

![passo6](./screenshots/acessando-int-web-pnet.png)

Abra o navegador e acesse o endereço IP exibido pela VM.

---

# Acessando os Cenários

![passo7](./screenshots/acessando-lab.png)

![passo8](./screenshots/dentro-lab.png)

Dentro do PnetLab já existem dois cenários pré-configurados.

Você pode:

- Criar novos cenários
- Modificar os cenários existentes
- Adaptar os laboratórios conforme sua necessidade
