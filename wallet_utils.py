import lwk


def initialize_network():
    """
    Inicializa e retorna a rede principal.
    """
    return lwk.Network.mainnet()

def check_wallet_balance(wollet):
    """
    Retorna o saldo atual da carteira watch-only.
    """
    return wollet.balance()

def create_wallet(seed_phrase=None):
    """
    Cria uma carteira a partir de uma frase semente fornecida ou gera uma nova.
    Retorna a carteira criada e a frase semente usada.
    """
    network = initialize_network()

    if seed_phrase is None:
        mnemonic = lwk.Mnemonic.generate()  # Gera uma nova frase semente
        seed_phrase = mnemonic.words().split()  # Converte para lista de palavras
    else:
        mnemonic = lwk.Mnemonic(" ".join(seed_phrase))  # Usa a frase semente fornecida

    signer = lwk.Signer(mnemonic, network)  # Instancia o signer com a frase semente
    desc = signer.wpkh_slip77_descriptor()  # Captura o descritor para a wallet

    # Cria a carteira (não mais watch-only) e faz o scan completo para atualizá-la
    wollet = lwk.Wollet(network, desc, datadir=None)
    client = network.default_electrum_client()
    update = client.full_scan(wollet)
    wollet.apply_update(update)
    
    return wollet, seed_phrase

def build_and_send_transaction(wollet, asset, recipient_address, asset_amount):
    """
    Constrói e envia uma transação para o endereço do destinatário com o ativo especificado.
    Retorna o ID da transação (txid).
    """
    builder = initialize_network().tx_builder()
    builder.add_recipient(recipient_address, asset_amount, asset)
    unsigned_pset = builder.finish(wollet)
    signer = lwk.Signer(wollet.signer.mnemonic, wollet.network)
    signed_pset = signer.sign(unsigned_pset)
    finalized_pset = wollet.finalize(signed_pset)
    tx = finalized_pset.extract_tx()
    client = wollet.network.default_electrum_client()
    txid = client.broadcast(tx)
    wollet.wait_for_tx(txid, client)
    return txid

def consultar_saldo_e_endereco(seed_mnemonic, indice):
    """
    seed_mnemonic: user uma lista ["cat", "cat", "cat", "cat", "cat", "cat", "cat", "cat", "cat", cat", "cat", "cat"] 
    indice: defina um valor inteiro (1,2,3,4...n) para retornar um saldo referente aquele endereço do indice
    """

    # Configuração da rede (Liquid Mainnet)
    network = lwk.Network.mainnet()

    # Criação do objeto Mnemonic e Signer
    mnemonic = lwk.Mnemonic(" ".join(seed_mnemonic))
    signer = lwk.Signer(mnemonic, network)
    desc = signer.wpkh_slip77_descriptor()

    # Criação da carteira apenas para visualização
    wollet = lwk.Wollet(network, desc, datadir=None)
    
    # Conexão com o cliente Electrum da blockchain
    client = network.default_electrum_client()
    
    # Atualização completa da carteira
    update = client.full_scan(wollet)
    wollet.apply_update(update)
    
    # Exibir endereço da carteira
    address = wollet.address(indice).address()
    
    return address

def saldo_assets(seed_mnemonic):
    network = lwk.Network.mainnet()  # Definindo rede principal
    mnemonic = lwk.Mnemonic(" ".join(seed_mnemonic))  # Instanciando objeto mnemonico
    client = network.default_electrum_client()  # Instanciando conexão com a blockchain
    signer = lwk.Signer(mnemonic, network)  # Instanciando signer
    desc = signer.wpkh_slip77_descriptor()  # Capturando descritor para watch-only

    wollet = lwk.Wollet(network, desc, datadir=None)  # Definindo wallet watch-only
    update = client.full_scan(wollet)  # Buscando atualizações da wallet
    wollet.apply_update(update)  # Aplicando atualizações na wallet watch-only
    saldos = wollet.balance()
    return saldos

def transacoes_recebidas(seed_mnemonic):
    """
    Lista todas as transações de recebimento com status (confirmada ou não).
    """
    network = lwk.Network.mainnet()
    mnemonic = lwk.Mnemonic(" ".join(seed_mnemonic))
    signer = lwk.Signer(mnemonic, network)
    desc = signer.wpkh_slip77_descriptor()
    wollet = lwk.Wollet(network, desc, datadir=None)

    transacoes = wollet.transactions()

    transacoes_recebidas = []
    for tx in transacoes:
        if tx.received > 0:
            transacoes_recebidas.append({
                "txid": tx.txid,
                "status": "confirmada" if tx.confirmed else "pendente",
                "bloco": tx.block_height,
                "valor_recebido": tx.received,
                "data": tx.confirmation_time
            })

    return transacoes_recebidas