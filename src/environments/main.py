from core.mad_rl import MAD_RL

if __name__ == "__main__":

    config = MAD_RL.config()
    engine = MAD_RL.engine()

    if config["train"] == True:
        engine.train()
    
    if config["test"] == True:
        engine.test()