---
title: Migrating a server to another region
date: 2026-10-01
---

# Migrating a server to another region

## Before you start

Check that the target region offers the server size you use. Every plan can use every region.

## Moving the server

A server cannot be moved between regions in place. Take a snapshot, copy it to the new region from the console, and create a server from the copy.

## After the move

The new server gets a new IP address, so update DNS records and firewall rules that name the old address.
