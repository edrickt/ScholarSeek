import pyterrier as pt
import os


class InformationRetriever:
    def __init__(self, name, stemmer, stopwords, tokeniser, dataset):
        self.name = name
        self.stemmer = stemmer
        self.stopwords = stopwords
        self.tokeniser = tokeniser
        self.dataset = dataset

        self.index_ref = None
        self.index_dir = self.createPath()

    def createPath(self):
        base_path = os.getcwd() + "/evaluation/indices/"
        return base_path + self.name

    def buildIndex(self):
        self.dataset = pt.get_dataset('irds:vaswani')
        if (os.path.exists(self.index_dir + "/data.properties") is False):
            indexer = pt.IterDictIndexer(self.index_dir, stemmer=self.stemmer, stopwords=self.stopwords, tokeniser=self.tokeniser)
            self.index_ref = indexer.index(self.dataset.get_corpus_iter(), fields=['text'])
        else:
            self.index_ref = pt.IndexRef.of(self.index_dir + "/data.properties")

    def search(self, model, query):
        if (self.index_ref is None):
            return False
        else:
            batchRetrieve = pt.BatchRetrieve(self.index_ref, wmodel=model)
            return batchRetrieve.search(query)


class Evaluator:
    def __init__(self, ir_systems):
        self.ir_systems = ir_systems
        self.dataset = self.checkSameDatasetAndAssign()

    def checkSameDatasetAndAssign(self):
        dataset = self.ir_systems[0].dataset
        for i in range(len(self.ir_systems)):
            if (dataset != self.ir_systems[i].dataset):
                return False
        return pt.get_dataset(dataset)

    def compareSystems(self, wmodel):
        pipelines = []
        for model in wmodel:
            for ir_system in self.ir_systems:
                ir = pt.BatchRetrieve(ir_system.index_ref, wmodel=model)
                pipelines.append(ir)

        results = pt.Experiment(
            pipelines,
            self.dataset.get_topics(),
            self.dataset.get_qrels(),
            eval_metrics=["num_rel_ret",
                          "mrt",
                          "recall_5",
                          "recall_10",
                          "recall_15",
                          "recall_20",
                          "recall_50",
                          "recall_100",
                          "P_5",
                          "P_10",
                          "P_15",
                          "P_20",
                          "P_50",
                          "P_100",
                          "map",
                          "recip_rank",
                          "ndcg"]
        )

        return results
    
    def runExperiment(self, wmodel):
        for ir_system in self.ir_systems:
            ir_system.buildIndex()

        results = self.compareSystems(wmodel)
        return results
    

class EnvironmentHandler:
    @staticmethod
    def SetJavaHome(dir):
        # /Users/edrickt/Documents/pyterrier-test/mac/jdk-21.0.1.jdk
        if (os.path.exists(dir)):
            os.environ["JAVA_HOME"] = dir
        elif (dir == "1"):
            os.environ["JAVA_HOME"] = "C:\Program Files\Java\jdk-21"


if __name__ == "__main__":
    EnvironmentHandler.SetJavaHome(input("Enter Java directory or leave empty for MacOS\n1: C:\Program Files\Java\jdk-21\nInput: "))

    if not pt.started():
        pt.init()
        pt.ApplicationSetup.setProperty("max.term.length", "500")

    ir_systems = [
        InformationRetriever(name="control", stemmer="porter", stopwords="terrier", tokeniser="english", dataset="irds:vaswani"),
        InformationRetriever(name="ir1", stemmer="none", stopwords="terrier", tokeniser="english", dataset="irds:vaswani"),
        InformationRetriever(name="ir2", stemmer="porter", stopwords="none", tokeniser="english", dataset="irds:vaswani"),
        InformationRetriever(name="ir3", stemmer="porter", stopwords="terrier", tokeniser="whitespace", dataset="irds:vaswani"),
        InformationRetriever(name="ir4", stemmer="none", stopwords="none", tokeniser="english", dataset="irds:vaswani"),
        InformationRetriever(name="ir5", stemmer="none", stopwords="terrier", tokeniser="whitespace", dataset="irds:vaswani"),
        InformationRetriever(name="ir6", stemmer="porter", stopwords="none", tokeniser="whitespace", dataset="irds:vaswani"),
        InformationRetriever(name="ir7", stemmer="none", stopwords="none", tokeniser="whitespace", dataset="irds:vaswani")
    ]

    ev = Evaluator(ir_systems)

    bm25_result = ev.runExperiment(wmodel=["BM25"])
    bm25_result.insert(0, "detail", ["control", "stm=n/a", "stp=n/a", "tkn=whtspc", "stm=n/a, stp=n/a", "stm=n/a, tkn=whtspc", "stp=n/a, tkn=whtspc", "stm=n/a, stp=n/a, tkn=whtspc"])

    tfidf_result = ev.runExperiment(wmodel=["TF_IDF"])
    tfidf_result.insert(0, "detail", ["control", "stm=n/a", "stp=n/a", "tkn=whtspc", "stm=n/a, stp=n/a", "stm=n/a, tkn=whtspc", "stp=n/a, tkn=whtspc", "stm=n/a, stp=n/a, tkn=whtspc"])

    tf_result = ev.runExperiment(wmodel=["Tf"])
    tf_result.insert(0, "detail", ["control", "stm=n/a", "stp=n/a", "tkn=whtspc", "stm=n/a, stp=n/a", "stm=n/a, tkn=whtspc", "stp=n/a, tkn=whtspc", "stm=n/a, stp=n/a, tkn=whtspc"])

    if (not os.path.exists(os.getcwd() + "/evaluation/results")):
        os.mkdir(os.getcwd() + "/evaluation/results", exist_ok=True)
        
    bm25_result.to_csv(os.getcwd() + "/evaluation/results/bm25.csv", sep="\t", index=False)
    tfidf_result.to_csv(os.getcwd() + "/evaluation/results/tfidf.csv", sep="\t", index=False)
    tf_result.to_csv(os.getcwd() + "/evaluation/results/tf.csv", sep="\t", index=False)
