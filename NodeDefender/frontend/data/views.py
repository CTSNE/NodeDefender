from .. import DataView
from .models import *
from flask import request, render_template

icpes = []
stats = []

@DataView.route('/data/power')
def DataPower():
    if request.method == 'GET':
        return render_template('data/power.html', icpes = icpes)

@DataView.route('/data/power/<mac>')
def DataPoweriCPE(mac):
    if request.method == 'GET':
        return render_template('data/powericpe.html', icpe = icpe)


@DataView.route('/data/power/<mac>/<nodeid>')
def DataPoweriCPENode(mac, nodeid):
    if request.method == 'GET':
        return render_template('data/powericpenode.html', icpe = icpe)


@DataView.route('/data/heat')
def DataHeat():
    if request.method == 'GET':
        return render_template('data/heat.html', stats = stats)

@DataView.route('/data/heat/<mac>')
def DataHeatiCPE(mac):
    if request.method == 'GET':
        return render_template('data/heaticpe.html', icpe = icpe)

@DataView.route('/data/heat/<mac>/<nodeid>')
def DataHeatiCPENode(mac, nodeid):
    if request.method == 'GET':
        return render_template('data/heaticpenode.html', icpe = icpe)

