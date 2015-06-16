import unittest
import zingchart.plots as plots
import pandas as pd


iris = pd.read_csv('data/iris.csv')


class TestBoxplotMethods(unittest.TestCase):
	def test_boxplot_dictionary_data(self):
		data = {}
		for f, df in iris.groupby("flower_type"):
			data[f] = df['petal length (cm)']
		expected = \
			{
			"type": "boxplot",
			"scaleX":
				{
				"values":
					["setosa", "versicolor", "virginica"]
				},
			"options": None,
			"series": [{
					   "data-box": [
						   [1.1374999999999995, 1.3999999999999999, 1.5, 1.5750000000000002, 1.8375000000000006],
						   [3.1000000000000005, 4.0, 4.3499999999999996, 4.5999999999999996, 5.4999999999999991],
						   [3.9374999999999978, 5.0999999999999996, 5.5499999999999998, 5.8750000000000009, 7.0375000000000032]],
					   "data-outlier": [
						   [0, 1.1000000000000001], [0, 1.0], [0, 1.8999999999999999],
						   [0, 1.8999999999999999], [1, 3.0]
					   ]
					   }]
			}

		result = plots.boxplot(data)
		self.assertAlmostEqual(expected, result)

	def test_boxplot_normal_data_1(self):
		data = iris[['petal length (cm)']]
		expected = {
		"type": "boxplot",
		"scaleX":
			{
				"values":
					["petal length (cm)"]
			},
		"options": None,
		"series": [{
					   "data-box": [
						   [-3.649999999999999, 1.6000000000000001, 4.3499999999999996, 5.0999999999999996, 10.349999999999998]],
					   "data-outlier": [
					   ]
				   }]
		}
		result = plots.boxplot(data)
		self.assertAlmostEqual(expected, result)

	def test_boxplot_normal_data_2(self):
		data = iris[['petal length (cm)', 'sepal width (cm)']]
		expected = {
		"type": "boxplot",
		"scaleX":
			{
				"values":
					["petal length (cm)", "sepal width (cm)"]
			},
		"options": None,
		"series": [{
					   "data-box": [
						   [-3.649999999999999, 1.6000000000000001, 4.3499999999999996, 5.0999999999999996, 10.349999999999998],
						   [2.0499999999999998, 2.7999999999999998, 3.0, 3.2999999999999998, 4.0499999999999998]],
					   "data-outlier": [[1, 4.4000000000000004], [1, 4.0999999999999996], [1, 4.2000000000000002], [1, 2.0]
					   ]
				   }]
		}
		result = plots.boxplot(data)
		self.assertAlmostEqual(expected, result)

	def test_hboxplot(self):
		data = {}
		expected = {
		"type": "hboxplot",
		"scaleX":{'values': []},
		"options":None,
		"series":[{'data-box': [], 'data-outlier': []}]
		}

		result = plots.boxplot(data, kind="hboxplot")
		self.assertAlmostEqual(expected, result)


suite = unittest.TestLoader().loadTestsFromTestCase(TestBoxplotMethods)
unittest.TextTestRunner(verbosity=2).run(suite)
